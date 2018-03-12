import re

from server.extensions import ser


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


def handle_message(msg):
    if 'time-' in msg:
        print('Message contains timestamp and gps data')
        print(msg)
        # call endpoint or just put the sutff here?


def serial_write(msg):
    ser.write(msg.encode('utf-8'))