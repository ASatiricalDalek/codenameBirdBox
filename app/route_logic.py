import time
#import picamera

def gen(camera):
    while True:
        frame = camera.get_frame()
        time.sleep(.12)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def instant_feed(motor, run):
    motor.spin(run)

