from flask import Blueprint, make_response, jsonify

error = Blueprint('error', __name__)


@error.errorhandler(Exception)
def internal_server_error(e):
    return make_response(jsonify({'error': str(e)}), 500)