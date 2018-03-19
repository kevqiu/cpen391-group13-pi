import os
import time

if os.uname()[4].startswith('arm'):
    # Running on the pi
    import picamera 
else:
    import cv2

class Camera:

    def __init__(self):
        self.img_dir = None

    def init_camera(self, img_dir):
        self.img_dir = img_dir

    def capture(self, img_id):
        # Running on the pi
        name = str(img_id) + '.jpeg'
        name = os.path.join(self.img_dir, name)
        print(name)
        if os.uname()[4].startswith('arm'):
            camera = picamera.PiCamera()
            camera.capture(name)
            camera.close()
        else:
            camera = cv2.VideoCapture(0)
            time.sleep(0.1)
            _, image = camera.read()
            cv2.imwrite(name, image)
            camera.release()
        return name
