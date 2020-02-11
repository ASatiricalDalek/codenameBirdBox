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


def check_feed():
    # This function is called every minute from a thread started in __init__
    # Gets the current time and converts it to a string we can do comparison against
    now = datetime.now()
    now_weekday = datetime.now().weekday() + 1
    format_now = now.strftime(str(now_weekday) +" %H %M")

    # TODO: Query the entire database, not just one user
    resultQuery = attributes.query.filter_by(scheduleFeed = 1).all()
    # TODO: Remove this print which is here for debug (leaving for now in case we need it later)
    #print(str(resultQuery.feedDays))
    # Query the DB and get the days the feeder should run. This will be returned as a string of numbers, w/ 1 being Mon
    # Ex: Feeder is supposed to run M W F. String from DB would be 135
    # i is the position in the string, v is the value in that position
    for query in resultQuery:
        print(str(query))
        print("Time now: "+format_now)
        for i, v in enumerate(str(query.feedDays)):
            # Create a string to match above in format Day Hour Minute. Hour and Minute pulled from DB entry directly
            result = v + " " + str(query.feedHour) + " " + str(query.feedMinute)
        else:
            print("Time Feed: "+result)
            # If the current time == the time in the DB run the motor
        if format_now == result:
            instant_feed(motor_pi.motor(), run=True)
    
    
    


# DB stores feed days as a string of integers, with 1 representing Monday, 2 representing Tuesday and so on
# Monday can't start at 0 because when this gets pulled from the DB Python interprets it as an int and drops leading 0s
# It is easier to pass nums as strings because the datetime function returns day of week as an integer
# See schedule_pi.py for more info
def get_feed_days(mon, tue, wed, thur, fri, sat, sun):
    feed_days = ""
    if mon:
        feed_days = feed_days + "1"
    if tue:
        feed_days = feed_days + "2"
    if wed:
        feed_days = feed_days + "3"
    if thur:
        feed_days = feed_days + "4"
    if fri:
        feed_days = feed_days + "5"
    if sat:
        feed_days = feed_days + "6"
    if sun:
        feed_days = feed_days + "7"
    return feed_days


# Settings Page Conversion Functions #
# These functions are for converting bools to ints for the form to the database, or vice versa for db to python logic
def convert_feed_from_form(feed_checkbox):
    if feed_checkbox:
        return 1
    else:
        return 0


def convert_feed_from_db(feed_query):
    if feed_query == 1:
        return True
    else:
        return False


# Radio buttons return string values
def convert_can_view_from_form(view_radio):
    if view_radio == 'True':
        return 1
    else:
        return 0


def convert_can_view_from_db(can_view_query):
    if can_view_query == 1:
        return True
    else:
        return False


# Radio buttons return string values
def convert_can_feed_from_form(feed_radio):
    if feed_radio == 'True':
        return 1
    else:
        return 0


def convert_can_feed_from_db(can_feed_query):
    if can_feed_query == 1:
        return True
    else:
        return False

# End Settings Conversion Functions #
