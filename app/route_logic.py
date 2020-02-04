import time
from datetime import datetime
from app import motor_pi

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

def check_feed(time):
    now = datetime.now()
    now_weekday = datetime.now().weekday()
    format_now = now.strftime(str(now_weekday) +" %H %M")
    print(format_now)
    if format_now == '1 15 38':
        instant_feed(motor_pi.motor(), run=True)



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
