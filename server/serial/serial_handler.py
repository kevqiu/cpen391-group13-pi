from datetime import datetime
import requests
import re

from server.modules import ser
from server.helpers.gps_helper import parse_gpgga_data, convert_dmm_to_dd


def serial_listener():
    """
    Serial thread to be spun up on server init
    Contains a buffer that stores incoming serial data.
    Calls handle_message when a \r is received
    """

    msg = ''
    if ser is not None:
        while True:
            for c in ser.read():
                char = chr(c)
                msg += char
                if char == '\r':
                    print('Serial message received: ' + msg)
                    handle_message(msg)
                    msg = ''


def handle_message(msg):
    """
    Handeles serial messages
    Message types:
    - init:time=HH:MM:SS
        - calls server to initialize autosort cycle
    - capture: gps=$GPGGA<gpgga data>
        - calls server to take image of object and save to database
    - done:time=HH:MM:SS,cycle_id=<ID>
    """

    # Auto sort is beginning
    if 'init:' in msg:
        (h, m, s) = [int(x) for x in re.findall(r'\d{2}:\d{2}:\d{2}', msg)[0].split(':')]
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        payload = {
            'start_time': dt_string
        }
        response = requests.post('http://localhost:5000/cycles', json=payload)
        serial_write('cycle_id={}\r'.format(response.json()['id']))

    # Image is ready to be scanned
    elif 'capture:' in msg:
        args = re.findall(r'(?<==)\S*', msg)
        try:
            data = parse_gpgga_data(args[0])
            dt = data.datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            payload = {
                'datetime': dt,
                'latitude': data.latitude if len(args) < 2 else convert_dmm_to_dd(args[1]),
                'longitude': data.longitude if len(args) < 2 else convert_dmm_to_dd(args[2])
            }
            requests.post('http://localhost:5000/capture/pi', json=payload)
        except:
            # send retry command to DE1
            serial_write('retry\r')
            print('Error attempting to parse GPGGA string')

    # Auto sort has completed
    elif 'done:' in msg:
        # update the existing cycle with the end time
        (h, m, s) = [int(x) for x in re.findall(r'\d{2}:\d{2}:\d{2}', msg)[0].split(':')]
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        cycle_id = int(re.findall(r'cycle_id=\d+', msg)[0].split('=')[1])
        payload = {
            'end_time': dt_string
        }
        requests.patch('http://localhost:5000/cycles/{}'.format(cycle_id), json=payload)

        # fetch the newly updated cycle and notify FCM
        cycle = requests.get('http://localhost:5000/cycles/{}'.format(cycle_id)).json()
        cycle['start_time'] = cycle['start_time'].replace('T', ' ').split('+')[0]
        cycle['end_time'] = cycle['end_time'].replace('T', ' ').split('+')[0]

        payload = {
            'topic': 'sort',
            'start_time': cycle['start_time'],
            'end_time': cycle['end_time']
        }
        requests.post('http://localhost:5000/notify', json=payload)

def serial_write(msg):
    if ser is not None:
        ser.write(msg.encode('utf-8'))