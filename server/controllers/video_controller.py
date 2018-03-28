from flask import Blueprint, Response
from server.modules import ca

video = Blueprint('video', __name__)


"""
GET video stream
"""
@video.route('/video_stream', methods=['GET'])
def video_feed():
    return Response(capture(ca), mimetype='multipart/x-mixed-replace; boundary=frame')


def capture(camera):
    while True:
        frame = ca.get_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytes(frame) + b'\r\n\r\n')



