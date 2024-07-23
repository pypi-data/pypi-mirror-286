#
# @author Sebastián Rodríguez Robotham
# Return datetime details
# @param difDates endDateTime - StartDateTime (long)
#
class HuemulDateTimePart:
    def __init__(self, difDates):
        milliseconds = difDates
        calc = difDates / 1000
        self.second = calc % 60
        calc /= 60
        self.minute = calc % 60
        calc /= 60
        self.hour = calc % 24
        calc /= 24
        self.days = calc

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)