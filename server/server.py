from flask import Flask
from threading import Thread

from server.config import DevConfig
from server.modules import db, ma, fcm, sc, ca, ml

from server.controllers.category_controller import categories
from server.controllers.error_controller import error
from server.controllers.controls_controller import controls
from server.controllers.warehouse_controller import warehouses
from server.controllers.item_controller import items
from server.controllers.notification_controller import notifications
from server.serial.serial_handler import serial_listener

""" Main app """
def create_app(config_object=DevConfig):
    # Flask app init
    app = Flask(__name__)
    app.config.from_object(config_object)

    print('Connecting to DB at {0}'.format(config_object.DB_PATH))

    # Module initialization
    # SQL Alchemy init
    db.init_app(app)
    # Marshmallow init
    ma.init_app(app)
    # ML Factory init
    ml.init_model(config_object)
    # Camera init
    ca.init_camera(config_object.IMG_PATH)
    # Serial connection init
    sc.init_serial(config_object.SERIAL_PORT, config_object.SERIAL_BAUDRATE)
    # FCM init
    fcm.init_push_service(config_object.FCM_API_KEY)

    # Blueprint registration
    app.register_blueprint(warehouses)
    app.register_blueprint(categories)
    app.register_blueprint(items)
    app.register_blueprint(controls)
    app.register_blueprint(notifications)
    app.register_blueprint(error)

    # Begin Serial thread
    thread = Thread(target=serial_listener)
    thread.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
