from app import motor_pi, route_logic, routes
import schedule
import time
from threading import Thread


class schedule_feed(Thread):  # The scheduled feeder thread TODO: give this info about the time to feed
    def __init__(self):  # Initalize the thread
        Thread.__init__(self)
        self.daemon = True
        self.start()
        
    def run(self):  # The code running in the thread
        #def job():
            #route_logic.instant_feed(motor_pi.motor(), run=True)  # Spins the motor
            
        #schedule.every(routes.minutes).minutes.do(job)  # Example: Every 1 minute spin the motor       
        while True:
            #schedule.run_pending()  # While the thread exists, keep checking every second if it is time to run the motor
            route_logic.check_feed(routes.minutes)
            time.sleep(60)
        
