from datetime import datetime

from flask import Blueprint, abort, request

from server.extensions import db, ser
from server.helpers.gps_helper import find_closest_warehouse
from server.models.item_model import Item
from server.models.warehouse_model import Warehouse

controls = Blueprint('controls', __name__)


"""
POST an item
Requires datetime, latitude, longitude in POST body as json
"""
@controls.route('/controls/capture', methods=['POST'])
def capture_image():
    dt = datetime.strptime(request.json.get('datetime'), "%Y-%m-%d %H:%M:%S.%f")
    lat = request.json.get('latitude')
    long = request.json.get('longitude')

    if not all((dt, lat, long)):
        abort(400, {'message: Missing data for item'})

    new_id = db.session.query(db.func.max(Item.id)).scalar() + 1

    # capture object and save image to storage
    # capture_image(new_id)

    # call ML and get category id
    category_id = 1
    #category_id = ML GOES HERE

    # get closest warehouse location
    closest_warehouse = find_closest_warehouse(Warehouse.query.all(), lat, long)

    # save item in DB
    item = Item(warehouse_id=closest_warehouse.id,
                category_id=category_id,
                datetime=dt,
                image_path='\images\{0}.jpeg'.format(new_id))
    db.session.add(item)
    db.session.commit()

    # return the category id to the DE1
    serial_write("cat:{0}\r".format(category_id))
    return ''


"""
POST Autosort
"""
@controls.route('/controls/autosort', methods=['POST'])
def autosort():
    serial_write('ctrl/as\r')
    return 'Beginning autosort'


"""
POST Stop
"""
@controls.route('/controls/stop', methods=['POST'])
def stop():
    serial_write('ctrl/st\r')
    return 'Stopping process'


"""
POST set position
"""
@controls.route('/controls/position/<int:pos>', methods=['POST'])
def override_position(pos):
    serial_write('ctrl/pos={0}\r'.format(pos))
    return 'Set to position ' + str(pos)


def serial_write(msg):
    if ser is not None:
        ser.write(msg.encode('utf-8'))
