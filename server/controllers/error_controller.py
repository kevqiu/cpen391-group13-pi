from flask import Blueprint, make_response, jsonify

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def err_404(e):
    return make_response(jsonify({'error': 'Route not found.'}), 404)


@error.errorhandler(Exception)
def internal_server_error(e):
    return make_response(jsonify({'error': str(e)}), 500)
