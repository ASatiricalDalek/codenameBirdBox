import logging
import time

# Basic log will be created at the start of the session
timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
logging.basicConfig(filename="log/"+str(timestr)+"-log.txt", level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
bbLog = logging.getLogger('bbLog')
bbLog.info("Creating session.")

# Logging will ignore flask related server messaging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
