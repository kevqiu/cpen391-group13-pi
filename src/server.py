import os
import sys

from flask import Flask

from config import Config, DevConfig
from src.controllers.category_controller import categories
from src.controllers.warehouse_controller import warehouses
from src.controllers.item_controller import items

from src.extensions import db, ma


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(warehouses)
    app.register_blueprint(categories)
    app.register_blueprint(items)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
