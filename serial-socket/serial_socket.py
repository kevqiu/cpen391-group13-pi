import serial

SERIAL_PORT = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 9600

ser = serial.Serial("/dev/ttyS0", baudrate=9600)
msg = ''

print("Serial connected!")

while True:
    for c in ser.read():
        char = chr(c)
        msg += char
        print(char)
        if char == '\r':
            print('Message: ' + msg)
            msg = ''
