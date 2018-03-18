import sys
from serial import Serial
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from machine_learning.scripts.ml_factory import MLFactory
from camera.camera import Camera

db = SQLAlchemy()
ma = Marshmallow()
ml = MLFactory()
ca = Camera()

SERIAL_PORT = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 9600

ser = None
try:
    ser = Serial("/dev/ttyS0", baudrate=9600)
    print('Serial port opened successfully!')
except:
    print('\nSerial port failed to be opened!\n', file=sys.stderr)
