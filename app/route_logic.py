import time


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

