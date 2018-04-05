from flask import Blueprint, json
from server.modules import ml
from server.config import DevConfig

from server.serial.serial_handler import serial_write

controls = Blueprint('controls', __name__)

@controls.route('/controls/model', methods=['GET'])
def get_ml_model():
    """
    GET model type
    """
    response = {
        'model': DevConfig.ML_MODEL_TO_USE.upper()
    }
    return json.dumps(response)

@controls.route('/controls/model/<model>', methods=['POST'])
def change_ml_model(model):
    """
    POST model type
    """
    DevConfig.ML_MODEL_TO_USE = model.lower()
    ml.init_model(DevConfig)
    return 'Model set: ' + model

@controls.route('/controls/autosort', methods=['POST'])
def autosort():
    """
    POST Autosort
    """
    serial_write('ctrl/as\r')
    return 'Beginning autosort'


@controls.route('/controls/stop', methods=['POST'])
def stop():
    """
    POST Stop
    """
    serial_write('ctrl/st\r')
    return 'Stopping process'


@controls.route('/controls/position/<int:pos>', methods=['POST'])
def override_position(pos):
    """
    POST set position
    Pos:
        position to set servo to
    """
    serial_write('ctrl/pos={0}\r'.format(pos))
    return 'Set to position ' + str(pos)

