from flask import Blueprint

from server.models.category_model import CategorySchema, Category

categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['GET'])
def get_all_categories():
    """
    GET All Categories
    """
    return CategorySchema(many=True).jsonify(Category.query.all())


@categories.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    """
    GET Category by Id
    """
    return CategorySchema().jsonify(Category.query.get(id))