from datetime import datetime
import requests
import re

from server.controllers.controls_controller import serial_write
from server.modules import ser
from server.helpers.gps_helper import parse_gpgga_data, convert_dmm_to_dd

""" 
Serial thread to be spun up on server init
Contains a buffer that stores incoming serial data.
Calls handle_message when a \r is received  
"""
def serial_listener():
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


""" 
Handeles serial messages
Message types:
- init:time=HH:MM:SS
    - calls server to initialize autosort cycle
- capture: gps=$GPGGA<gpgga data>
    - calls server to take image of object and save to database
- done:time=HH:MM:SS,cycle_id=<ID>
"""
def handle_message(msg):
    if 'init:' in msg:
        (h, m, s) = re.findall(r'\d{2}:\d{2}:\d{2}', msg).split(':')
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
        payload = {
            'start_time': dt_string
        }
        cycle_id = requests.post('http://localhost:5000/cycles',
                      json=payload)
        serial_write('cycle_id={}'.format(cycle_id))

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
            requests.post('http://localhost:5000/controls/capture',
                          json=payload)
        except:
            print('Error attempting to parse GPGGA string')

    elif 'done:' in msg:
        (h, m, s) = re.findall(r'\d{2}:\d{2}:\d{2}', msg).split(':')
        dt = datetime.now().replace(hour=h, minute=m, second=s)
        dt_string = dt.strftime("%Y-%m-%d %H:%M:%S.%f")

        cycle_id = int(re.findall(r'cycle_id=\d+', msg).split('='))

        payload = {
            'end_time': dt_string
        }

        requests.patch('http://localhost:5000/cycles/{}'.format(cycle_id),
                       json=payload)

        # values = re.findall('(?<==)\d+', msg)
        # payload = {
        #     'red': values[0],
        #     'green': values[1],
        #     'blue': values[2],
        #     'other': values[3]
        # }
        # requests.post('http://localhost:5000/notify',
        #                   json=payload)
