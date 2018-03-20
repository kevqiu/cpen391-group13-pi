import requests
import re

from server.extensions import ser
from server.helpers.gps_helper import parse_gpgga_data

""" 
Serial thread to be spun up on server init
Contains a buffer that stores incoming serial data.
Calls handle_message when a \r is received  
"""
def serial_listener():
    msg = ''
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
- capture: gps=$GPGGA<gpgga data>
    - calls server to take image of object and save to database
- done:r=<r_count>,g=<g_count>,g=<g_count>,o=<o_count>
"""
def handle_message(msg):
    if 'capture: gps=$GPGGA' in msg:
        gpgga_data = msg.split('gps=')[1]
        try:
            data = parse_gpgga_data(gpgga_data)
            payload = {
                'datetime': data.datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                'latitude': data.latitude,
                'longitude': data.longitude
            }
            requests.post('http://localhost:5000/controls/capture',
                          json=payload)
        except:
            print('Error attempting to parse GPGGA string')

    elif 'done:' in msg:
        values = re.search('(?<==)\d+', msg)

        payload = {
            'red': values[0],
            'green': values[1],
            'blue': values[2],
            'other': values[3]
        }

        requests.post('http://localhost:5000/notify',
                          json=payload)