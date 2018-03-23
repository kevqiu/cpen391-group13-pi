import requests
import re

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
- capture: gps=$GPGGA<gpgga data>
    - calls server to take image of object and save to database
- done:r=<r_count>,g=<g_count>,g=<g_count>,o=<o_count>
"""
def handle_message(msg):
    if 'capture:' in msg:
        args = re.findall(r'(?<==)\S*', msg)
        try:
            data = parse_gpgga_data(args[0])
            payload = {
                'datetime': data.datetime.strftime("%Y-%m-%d %H:%M:%S.%f"),
                'latitude': data.latitude if len(args) < 2 else convert_dmm_to_dd(args[1]),
                'longitude': data.longitude if len(args) < 2 else convert_dmm_to_dd(args[2])
            }
            requests.post('http://localhost:5000/controls/capture',
                          json=payload)
        except:
            print('Error attempting to parse GPGGA string')

    elif 'done:' in msg:
        values = re.findall('(?<==)\d+', msg)
        payload = {
            'red': values[0],
            'green': values[1],
            'blue': values[2],
            'other': values[3]
        }
        requests.post('http://localhost:5000/notify',
                          json=payload)
