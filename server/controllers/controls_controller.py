from flask import Blueprint

from server.serial.serial_handler import serial_write

controls = Blueprint('controls', __name__)


"""
POST Autosort
"""
@controls.route('/controls/autosort', methods=['POST'])
def autosort():
    serial_write('ctrl/as\r')
    return 'Beginning autosort'


"""
POST Stop
"""
@controls.route('/controls/stop', methods=['POST'])
def stop():
    serial_write('ctrl/st\r')
    return 'Stopping process'


"""
POST set position
"""
@controls.route('/controls/position/<int:pos>', methods=['POST'])
def override_position(pos):
    serial_write('ctrl/pos={0}\r'.format(pos))
    return 'Set to position ' + str(pos)

