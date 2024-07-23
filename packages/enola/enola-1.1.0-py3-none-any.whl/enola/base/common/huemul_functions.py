from datetime import datetime, timezone

class HuemulFunctions:
    def __init__(self):
        self.started = True
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    #
    # getCurrentDateTime: returns current datetime
    # from version 1.1
    #
    def get_current_datetime_java(self):
        return datetime.now(timezone.utc)

    # return datetime in log format
    # date: datetime.now(timezone.utc)
    # return string
    def get_date_for_log(self, date):
        #dateTimeFormat: DateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS")
        dateString = date.isoformat(timespec='milliseconds')

        return dateString

    # return date in string format
    # date
    def get_date_for_api(self):
        #dateTimeFormat: DateFormat = new SimpleDateFormat("yyyy-MM-ddTHH:mm:ss:SSSz")
        newDate = datetime.now(timezone.utc)
        dateString = newDate.isoformat(timespec='milliseconds')

        return dateString
    
    def get_dif_seconds(self, dateFromIso, dateToIso):
        dateFrom = datetime.fromisoformat(dateFromIso)
        dateTo = datetime.fromisoformat(dateToIso)
        return (dateTo - dateFrom).total_seconds()
    
    def get_dif_ms(self, dateFromIso, dateToIso):
        dateFrom = datetime.fromisoformat(dateFromIso)
        dateTo = datetime.fromisoformat(dateToIso)
        return (dateTo - dateFrom).total_seconds() * 1000

    def delete_args(self, data):
        try:
            delattr(data, "args")
        except:
            a = None