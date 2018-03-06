import sys
from flask import Blueprint, jsonify

from src.models.warehouse_model import WarehouseSchema, Warehouse

warehouses = Blueprint('warehouses', __name__)


@warehouses.route('/warehouses', methods=['GET'])
def get_all_warehouses():
    w = Warehouse.query.all()
    return WarehouseSchema(many=True).jsonify(Warehouse.query.all())
