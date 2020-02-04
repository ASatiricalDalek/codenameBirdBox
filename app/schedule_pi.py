from app import motor_pi, route_logic, routes
from app.models import *
import time
from threading import Thread


class schedule_feed(Thread):  # The scheduled feeder thread TODO: give this info about the time to feed
    def __init__(self):  # Initalize the thread
        Thread.__init__(self)
        self.daemon = True
        self.start()
        
    def run(self):  # The code running in the thread     
        while True:
            route_logic.check_feed()
            time.sleep(60)
        
