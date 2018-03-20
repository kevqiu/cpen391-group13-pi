import sys
from flask import Blueprint

from server.models.warehouse_model import WarehouseSchema, Warehouse

warehouses = Blueprint('warehouses', __name__)


"""
GET All Warehouses
"""
@warehouses.route('/warehouses', methods=['GET'])
def get_all_warehouses():
    return WarehouseSchema(many=True).jsonify(Warehouse.query.all())


"""
GET Warehouse by Id
"""
@warehouses.route('/warehouses/<int:id>', methods=['GET'])
def get_warehouse(id):
    return WarehouseSchema().jsonify(Warehouse.query.get(id))