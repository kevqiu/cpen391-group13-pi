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
    Serial message handling
    Message types:
    - init:time=HH:MM:SS
        - calls server to initialize autosort cycle
    - capture: gps=<gpgga sentence> (optional: mock_lat=<lat> mock_lng=<lng>)
        - calls server to take image of object and save to database
    - done:time=HH:MM:SS,cycle_id=<ID>
    """

    # Auto sort is beginning
    if 'init:' in msg:
        # regex select on timestamp in HH:MM:SS format
        (h, m, s) = [int(x) for x in re.findall(r'\d{2}:\d{2}:\d{2}', msg)[0].split(':')]

        # init on current time, replacing timestamp with GPS time
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        # create POST payload and create new cycle
        payload = {
            'start_time': dt_string
        }
        response = requests.post('http://localhost:5000/cycles', json=payload)

        # return the cycle id to the DE1 for storage
        serial_write('cycle_id={}\r'.format(response.json()['id']))

    # Image is ready to be scanned
    elif 'capture:' in msg:
        # regex select on values between = and whitespace
        args = re.findall(r'(?<==)\S*', msg)
        try:
            # obtain NMEA data from GPGGA sentence
            data = parse_gpgga_data(args[0])
            # convert datetime to server-friendly format
            dt = data.datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

            # create POST payload, use mock location if provided, and scan image
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
        # regex select on timestamp in HH:MM:SS format
        (h, m, s) = [int(x) for x in re.findall(r'\d{2}:\d{2}:\d{2}', msg)[0].split(':')]

        # init on current time, replacing timestamp with GPS time
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        # get cycle id the DE1 stored
        cycle_id = int(re.findall(r'cycle_id=\d+', msg)[0].split('=')[1])

        # update the existing cycle with the end time
        payload = {
            'end_time': dt_string
        }
        requests.patch('http://localhost:5000/cycles/{}'.format(cycle_id), json=payload)

        # fetch the newly updated cycle and notify FCM
        cycle = requests.get('http://localhost:5000/cycles/{}'.format(cycle_id)).json()
        cycle['start_time'] = cycle['start_time'].replace('T', ' ').split('+')[0]
        cycle['end_time'] = cycle['end_time'].replace('T', ' ').split('+')[0]

        # notify app with cycle time range
        payload = {
            'topic': 'sort',
            'start_time': cycle['start_time'],
            'end_time': cycle['end_time']
        }
        requests.post('http://localhost:5000/notify', json=payload)


def serial_write(msg):
    """Helper to write to serial port"""
    if ser is not None:
        ser.write(msg.encode('utf-8'))