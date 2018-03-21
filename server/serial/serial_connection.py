import sys
from serial import Serial


class SerialConnection:

    def __init__(self):
        self.serial = None


    def init_serial(self, port, baudrate):
        try:
            self.serial = Serial(port=port, baudrate=baudrate)
            print('Serial port opened successfully!')
        except:
            print('\nSerial port failed to be opened!\n', file=sys.stderr)

