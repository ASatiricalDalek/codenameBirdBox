import time
from app.models import *


# This continuously captures images to feed the _thread function in BaseCamera.py
def gen(camera):
    while True:
        frame = camera.get_frame()
        time.sleep(.12)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# This executes the motor spin script in motor_pi.py
def instant_feed(motor, run):
    motor.spin(run)


def canView(uid):
    usr = attributes.query.filter_by(userID=uid).first()
    if usr.canView == 1:
        return True
    else:
        return False


def canFeed(uid):
    usr = attributes.query.filter_by(userID=uid).first()
    if usr.canFeed == 1:
        return True
    else:
        return False
