from flask import Blueprint

control = Blueprint('control', __name__)

@control.route("/classify")
def classify():
    return "classifying"