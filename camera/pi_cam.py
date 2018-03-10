import picamera


def capture_img(id):
    camera = picamera.PiCamera()
    name = str(id)+".jpeg"
    camera.capture(name)