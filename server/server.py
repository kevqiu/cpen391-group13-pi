from flask import Flask

from server.config import DevConfig
from server.controllers.category_controller import categories
from server.controllers.error_controller import error
from server.controllers.warehouse_controller import warehouses
from server.controllers.item_controller import items
from server.extensions import db, ma


""" Main app """
def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    print('Connecting to DB at {0}'.format(config_object.DB_PATH))

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(warehouses)
    app.register_blueprint(categories)
    app.register_blueprint(items)
    app.register_blueprint(error)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
