import config

from flask import Blueprint
from ..repositories.data_repository import DataRepository

repository = DataRepository(config.db_path)

data = Blueprint('data', __name__)

@data.route("/items")
def itemsList():
    return repository.get_items()

# @data.route("/test")
# def test():
#     return repository.get_items_test()