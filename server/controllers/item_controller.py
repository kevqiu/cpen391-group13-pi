import os
from flask import Blueprint, request, send_file, make_response, jsonify

from server.models.item_model import ItemSchema, Item
from server.config import DevConfig

items = Blueprint('items', __name__)


"""
GET All Items with support for filtering on warehouse and category id
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
    path = '{0}\{1}.jpeg'.format(DevConfig.IMG_PATH, id)
    if os.path.isfile('{0}\{1}.jpeg'.format(DevConfig.IMG_PATH, id)):
        return send_file(path, mimetype='image/jpeg')
    else:
        return make_response(jsonify({'error': 'Image not found on server'}), 404)
