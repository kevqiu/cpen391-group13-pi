import sys
from flask import Blueprint

from server.models.item_model import ItemSchema, Item

items = Blueprint('items', __name__)


@items.route('/items', methods=['GET'])
def get_all_items():
    i = ItemSchema(many=True).jsonify(Item.query.all())
    print(i.data)
    return ItemSchema(many=True).jsonify(Item.query.all())
