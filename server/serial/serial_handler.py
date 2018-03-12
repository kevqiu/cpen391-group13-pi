from server.controllers.controls_controller import capture_image
from server.extensions import ser
from server.helpers.gps_helper import parse_gpgga_data


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


""" Handeles serial messages
Message format:
capture: gps=$GPGGA<gpgga data>
"""
def handle_message(msg):
    if 'capture: gps=' in msg:
        gpgga_data = msg.split('gps=')[1]
        data = parse_gpgga_data(gpgga_data)
        # data = None
        capture_image(data)
