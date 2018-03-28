import platform 
import os
import time

if platform.uname()[4].startswith('arm'):
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
        name = str(img_id) + '.jpeg'
        name = os.path.join(self.img_dir, name)
        if platform.uname()[4].startswith('arm'):
            # Running on the pi
            camera = picamera.PiCamera()
            camera.capture(name)
            camera.close()
        else:
            camera = cv2.VideoCapture(1)
            time.sleep(0.1)
            _, image = camera.read()
            cv2.imwrite(name, image)
            camera.release()
        return name

    def get_image(self):
        if platform.uname()[4].startswith('arm'):
            # TODO: Implement
            raise BaseException('Is not implemented')
            return ""
        else:
            camera = cv2.VideoCapture(0)
            _, image = camera.read()
            frame = cv2.resize(image, (100, 27))
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg

