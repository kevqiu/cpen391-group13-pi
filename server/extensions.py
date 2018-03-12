from serial import Serial
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

SERIAL_PORT = '/dev/ttyAMA0'
SERIAL_BAUDRATE = 9600
ser = Serial("/dev/ttyS0", baudrate=9600)

