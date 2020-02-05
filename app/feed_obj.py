from datetime import datetime


class FeedTimeObject:
    def __init__(self):
        self.feed_time = None
        self.feed_days = None
        self.feed_creator = None

    def set_feed_time(self, feed_time):
        d = datetime.strptime(feed_time, "%H:%M")
        self.feed_time = d.strftime("%I:%M %p")

    def set_feed_days(self, feed_days):
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
