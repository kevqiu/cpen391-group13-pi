from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from machine_learning.scripts.ml_factory import MLFactory
from camera.camera import Camera
from server.fcm.fcm import FCM
from server.serial.serial_connection import SerialConnection

db = SQLAlchemy()
ma = Marshmallow()
ml = MLFactory()
ca = Camera()
fcm = FCM()
sc = SerialConnection()
