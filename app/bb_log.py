import logging
import time
import os
import shutil


def log_path():
    if os.path.isdir(str(os.getcwd())+'/log'):
        shutil.rmtree(str(os.getcwd())+'/log')  # removes log directory and files contained within
        os.mkdir(str(os.getcwd())+'/log')  # Created log directory for the log file associated with the current session
        log_format()  # define log format
    else:
        os.mkdir(str(os.getcwd()) + '/log')  # Create the log directory if it did not already exist
        log_format()  # define log format


def log_format():
    timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename="log/" + str(timestr) + "-log.txt", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Basic log will be created at the start of the session
log_path()
bbLog = logging.getLogger('bbLog')
# Logging will ignore flask related server messaging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

bbLog.info("Creating session. Ignoring server messaging.")

