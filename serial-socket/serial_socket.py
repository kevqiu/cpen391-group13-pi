import serial

SERIAL_PORT = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 9600

ser = serial.Serial("/dev/ttyS0", baudrate=9600)
msg = []

while True:
    for c in ser.read():
        msg.append(c)
        if c == '\r':
            print('Message: ' + msg)
            msg = []