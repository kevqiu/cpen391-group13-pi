import sys
from flask import Blueprint, request

from server.models.item_model import ItemSchema, Item

items = Blueprint('items', __name__)


@items.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query

    warehouse_query = request.args.get('warehouse_id')
    if warehouse_query != None:
        items = items.filter(Item.warehouse_id == warehouse_query)

    category_query = request.args.get('category_id')
    if category_query != None:
        items = items.filter(Item.category_id == category_query)

    return ItemSchema(many=True).jsonify(items)


@items.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    return ItemSchema().jsonify(Item.query.get(id))
