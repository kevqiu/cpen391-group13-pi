from datetime import datetime

from flask import Blueprint, abort

from server.extensions import db, ser
from server.helpers.gps_helper import find_closest_warehouse
from server.models.item_data import ItemData
from server.models.item_model import Item
from server.models.warehouse_model import Warehouse

controls = Blueprint('controls', __name__)


# @controls.route('/controls/capture', methods=['POST'])
def capture_image(data):
    # dummy data, location is in Ottawa
    # data = ItemData(datetime.now(), 45.2497533, -76.3606651)

    new_id = db.session.query(db.func.max(Item.id)).scalar() + 1

    # capture object and save image to storage
    # capture_image(new_id)

    # call ML and get category id
    category_id = 1
    #category_id = ML GOES HERE

    # get closest warehouse location
    closest_warehouse = find_closest_warehouse(Warehouse.query.all(), data)

    # save item in DB
    item = Item(warehouse_id=closest_warehouse.id,
                category_id=category_id,
                datetime=data.datetime,
                image_path='\images\{0}.jpeg'.format(new_id))
    db.session.add(item)
    db.session.commit()
    return ''


@controls.route('/controls/autosort/<int:status>', methods=['POST'])
def autosort(status):
    if status == 0 or status == 1:
        serial_write('ctrl:as={0}\r'.format(status))
        return 'Autosort enabled'
    else:
        abort(400, {'message': 'Invalid autosort status: <{0}>. '
                               'Valid inputs are 0, 1'.format(status)})


@controls.route('/controls/position/<int:pos>', methods=['POST'])
def override_position(pos):
    serial_write('ctrl:pos={0}\r'.format(pos))
    return 'Set to position ' + str(pos)


def serial_write(msg):
    ser.write(msg.encode('utf-8'))
