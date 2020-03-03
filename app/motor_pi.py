import RPi.GPIO as GPIO
import time


class motor:
    # This function handles the spinning of the servo motor
    def spin(self, run):
        if run:
            servoPIN = 17  # Corresponds to GPIO pin 11 on the Raspberry Pi 3 B+
            # GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number,
            # these are the numbers after "GPIO" in the green rectangles for GPIO config. on Raspberry Pi schematic
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servoPIN, GPIO.OUT)  # Set GPIO17 as the output
            t_end = time.time() + 2 * 1  # Execute for (2s*1m) from time script executes then stop
            p = GPIO.PWM(servoPIN, 10)  # Create PWN instance on GPIO 17 for Pulse width modulation with 10Hz
            GPIO.setwarnings(False)  # Ignores warnings when using GPIO library
            p.start(2.5)  # Initialization (2.5% of 10Hz)
            try:
                while time.time() < t_end:  # Runs for 2 seconds after the current time
                    p.ChangeDutyCycle(5)  # To adjust the value of the PWM output (ex. 5% of 10Hz)
                    time.sleep(0.5)  # Do nothing for .5 second
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
                    p.stop()  # Turn off PWN on GPIO17
                    GPIO.cleanup()  # Release any resources the script may be using
            except KeyboardInterrupt:
                p.stop()
                GPIO.cleanup()
