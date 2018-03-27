import sys
from serial import Serial
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from machine_learning.scripts.ml_factory import MLFactory
from camera.camera import Camera
from server.fcm.fcm import FCM

db = SQLAlchemy()
ma = Marshmallow()
ml = MLFactory()
ca = Camera()
fcm = FCM()

SERIAL_PORT = '/dev/ttyS0'
SERIAL_BAUDRATE = 9600

ser = None
try:
    ser = Serial(port=SERIAL_PORT, baudrate=SERIAL_BAUDRATE)
    print('Serial port opened successfully!')
except:
    print('\nSerial port failed to be opened!\n', file=sys.stderr)
