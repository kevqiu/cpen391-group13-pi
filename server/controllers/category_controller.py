from flask import Blueprint

from server.models.category_model import CategorySchema, Category

categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['GET'])
def get_all_categories():
    return CategorySchema(many=True).jsonify(Category.query.all())
