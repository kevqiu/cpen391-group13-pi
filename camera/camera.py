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
        self._cam = None

    def init_camera(self, img_dir):
        self.img_dir = img_dir
        if platform.uname()[4].startswith('arm'):
        # Running on the pi
            self._cam = picamera.PiCamera()
            self._cam.brightness = 45   
        else:
            self._cam = cv2.VideoCapture(1)


    def capture(self, img_id):
        name = str(img_id) + '.jpeg'
        name = os.path.join(self.img_dir, name)
        if platform.uname()[4].startswith('arm'):
            time.sleep(0.1)
            self._cam.capture(name)
            time.sleep(0.1)
        else:
            _, image = self._cam.read()
            cv2.imwrite(name, image)
        return name

    def get_image(self):
        if platform.uname()[4].startswith('arm'):
            # TODO: Implement
            raise BaseException('Is not implemented')
            return ""
        else:
            _, image = self._cam.read()
            frame = cv2.resize(image, (320, 180))
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg

