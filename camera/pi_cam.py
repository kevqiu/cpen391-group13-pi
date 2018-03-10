import  picamera
import time

def capture_img(id):
    camera = picamera.PiCamera()
    name = str(id)+".jpeg"
    camera.capture(name)

capture_img(119)