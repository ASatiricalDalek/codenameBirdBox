from datetime import datetime


class FeedTimeObject:
    def __init__(self):
        # Allow creation of an empty object (to be filled later)
        self.feed_time = None
        self.feed_days = None
        self.feed_creator = None

    def set_feed_time(self, feed_time):
        # Feed time in the DB is set in 24 hour time. This setter converts to 12 hr
        d = datetime.strptime(feed_time, "%H:%M")
        self.feed_time = d.strftime("%I:%M %p")

    def set_feed_days(self, feed_days):
        # feed days are a string of number in the DB. This converts them to human readable dates
        nice_days = []
        for i, v in enumerate(str(feed_days)):
            if v == '1':
                nice_days.append("Mon")
            if v == '2':
                nice_days.append("Tues")
            if v == '3':
                nice_days.append("Wed")
            if v == '4':
                nice_days.append("Thur")
            if v == '5':
                nice_days.append("Fri")
            if v == '6':
                nice_days.append("Sat")
            if v == '7':
                nice_days.append("Sun")
            self.feed_days = nice_days

    def set_feed_creator(self, feed_creator):
        self.feed_creator = feed_creator
