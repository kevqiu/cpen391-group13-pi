from datetime import datetime, timedelta

from flask import Flask

from server.config import DevConfig
from server.models.cycle_model import Cycle
from server.modules import db
from server.models.category_model import Category
from server.models.item_model import Item
from server.models.warehouse_model import Warehouse

""" Database table creation. Invoked by adding -db flag to script execution """
def init_db(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    print('Connecting to DB at {0}'.format(config_object.DB_PATH))

    with app.app_context():
        db.init_app(app)

        db.reflect()
        db.drop_all()

        db.create_all()

        for d in data:
            db.session.add(d)
            print('Adding: {0}'.format(d))

        db.session.commit()

    print('Database successfully initialized!')

# data that database uses to populate
data = [
    Warehouse(location='UBC', latitude=49.2616035, longitude='-123.2498017'),
    Warehouse(location='UofT', latitude=43.6600823, longitude='-79.39534'),
    Warehouse(location='McGill', latitude=45.5060011, longitude='-73.5764305'),

    Category(category='red'),
    Category(category='green'),
    Category(category='blue'),
    Category(category='other'),

#    Cycle(start_time=datetime.now() - timedelta(days=1), end_time=datetime.now()),

 #   Item(warehouse_id=1, category_id=1, datetime=datetime.now() - timedelta(days=3)),
 #   Item(warehouse_id=1, category_id=1, datetime=datetime.now() - timedelta(days=2)),
 #   Item(warehouse_id=1, category_id=1, datetime=datetime.now() - timedelta(days=1)),
 #   Item(warehouse_id=1, category_id=1, datetime=datetime.now()),
]
