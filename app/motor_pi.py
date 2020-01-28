import RPi.GPIO as GPIO
import time


class motor:

    def spin(self, run):
        if run:
            servoPIN = 17
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servoPIN, GPIO.OUT)
            t_end = time.time() + 2 * 1  # Execute for (30s*1m) from time script ececutes then stop
            p = GPIO.PWM(servoPIN, 10)  # GPIO 17 for PWM with 10Hz
            GPIO.setwarnings(False)

            p.start(2.5)  # Initialization
            try:
                while time.time() < t_end:
                    p.ChangeDutyCycle(5)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(7.5)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(10)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(12.5)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(10)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(7.5)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(5)
                    time.sleep(0.5)
                    p.ChangeDutyCycle(2.5)
                    time.sleep(0.5)
                else:
                    p.stop()
                    GPIO.cleanup()
            except KeyboardInterrupt:
                p.stop()
                GPIO.cleanup()
