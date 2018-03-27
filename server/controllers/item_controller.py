import urllib.parse
from datetime import datetime
import os

from flask import Blueprint, request, send_file

from server.config import DevConfig
from server.models.item_model import ItemSchema, Item

items = Blueprint('items', __name__)


"""
GET All Items
Support filtering: 
    - warehouse_id: int
    - category_id: int
    - between: YY-mm-ddTHH:MM:SS.fffff,YY-mm-ddTHH:MM:SS.fffff
        (exclude the timezone change in the query, Python doesn't support RFC 3339 format)
"""
@items.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query

    # filter on warehouse_id
    warehouse_query = request.args.get('warehouse_id')
    if warehouse_query is not None:
        items = items.filter(Item.warehouse_id == warehouse_query)

    # filter on category_id
    category_query = request.args.get('category_id')
    if category_query is not None:
        items = items.filter(Item.category_id == category_query)

    # filter on time_between
    time_query = request.args.get('between')
    if time_query is not None:
        time_query_decoded = urllib.parse.unquote(time_query)
        print(time_query_decoded)
        (start, end) = [datetime.strptime(t.replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f') for t in time_query_decoded.split(',')]
        items = items.filter(Item.datetime.between(start, end))

    return ItemSchema(many=True).jsonify(items)


"""
GET Item by ID
"""
@items.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    return ItemSchema().jsonify(Item.query.get(id))


"""
GET Item Image by ID
"""
@items.route('/items/<int:id>/image', methods=['GET'])
def get_item_image(id):
    img_file = '{0}.jpeg'.format(id)
    img_path = os.path.join(DevConfig.IMG_PATH, img_file)
    if os.path.isfile(img_path):
        return send_file(img_path, mimetype='image/jpeg')
    else:
        return send_file(os.path.join(DevConfig.IMG_PATH, 'no_image.jpeg'), mimetype='image/jpeg')
