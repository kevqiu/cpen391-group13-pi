from flask import Blueprint

from server.modules import ser

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


def serial_write(msg):
    if ser is not None:
        ser.write(msg.encode('utf-8'))
