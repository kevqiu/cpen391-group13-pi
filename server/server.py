from flask import Flask
from threading import Thread

from server.config import DevConfig
from server.extensions import db, ma

from server.controllers.category_controller import categories
from server.controllers.error_controller import error
from server.controllers.controls_controller import controls
from server.controllers.warehouse_controller import warehouses
from server.controllers.item_controller import items
from server.serial.serial_listener import serial_listener

""" Main app """
def create_app(config_object=DevConfig):
    # Flask app init
    app = Flask(__name__)
    app.config.from_object(config_object)

    print('Connecting to DB at {0}'.format(config_object.DB_PATH))

    # Extension init
    db.init_app(app)
    ma.init_app(app)

    # Blueprint registration
    app.register_blueprint(warehouses)
    app.register_blueprint(categories)
    app.register_blueprint(items)
    app.register_blueprint(controls)
    app.register_blueprint(error)

    # Begin Serial thread
    thread = Thread(target=serial_listener)
    thread.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
