import os
import time
from server import config

if os.uname()[4].startswith('arm'):
    # Running on the pi
    import picamera 
else:
    import cv2

def camera_capture(img_id):
    # Running on the pi
    name = str(img_id) + '.jpeg'
    name = os.path.join(config.DevConfig.IMG_PATH, name)
    print(name)
    if os.uname()[4].startswith('arm'):
        camera = picamera.PiCamera()
        camera.capture(name)
    else:
        camera = cv2.VideoCapture(0)
        time.sleep(0.1)
        _, image = camera.read()
        cv2.imwrite(name, image)
        camera.release()
    return name
