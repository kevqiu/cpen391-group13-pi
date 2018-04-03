import sys
from flask import Blueprint

from server.models.warehouse_model import WarehouseSchema, Warehouse

warehouses = Blueprint('warehouses', __name__)


@warehouses.route('/warehouses', methods=['GET'])
def get_all_warehouses():
    """
    GET All Warehouses
    """

    return WarehouseSchema(many=True).jsonify(Warehouse.query.all())


@warehouses.route('/warehouses/<int:id>', methods=['GET'])
def get_warehouse(id):
    """
    GET Warehouse by Id
    """

    return WarehouseSchema().jsonify(Warehouse.query.get(id))