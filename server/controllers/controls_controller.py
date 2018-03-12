from flask import Blueprint, abort

from server.extensions import ser
from server.models.item_model import Item
from server.serial.serial_listener import serial_write

controls = Blueprint('contorls', __name__)


@controls.route('/controls/capture', methods=['POST'])
def capture_image(data):
    # call camera script and get path
    img_path = r'\images\test.jpeg'

    # call ML and get category id

    # get warehouse location

    # save item in DB
    item = Item(warehouse_id=1, category_id=1, timestamp=0, image_path=img_path)
    # db.session.add(item)
    # db.session.commit()
    return ''


@controls.route('/controls/autosort/<int:status>', methods=['POST'])
def autosort(status):
    if status == 0 or status == 1:
        serial_write('ctrl:as-{0}'.format(status))
        return 'Autosort enabled'
    else:
        abort(400, {'message': 'Invalid autosort status: <{0}>. '
                               'Valid inputs are 0, 1'.format(status)})


@controls.route('/controls/position/<int:pos>', methods=['POST'])
def override_position(pos):
    serial_write('ctrl:{0}'.format(pos))
    return 'Set to position ' + pos
