from flask import Blueprint

from server.extensions import ser
from server.models.item_model import Item

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

@controls.route('/controls/override/<string:control>', methods=['POST'])
def capture_image(control):
    ser.write('ctrl:' + control)
    return ''
