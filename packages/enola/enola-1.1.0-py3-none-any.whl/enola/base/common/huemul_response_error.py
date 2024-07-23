#
# @author Sebastián Rodríguez Robotham
# error class used by backend to return error info
# @param errorId error Id
# @param errorTxt error Message
#
class HuemulResponseError:
    def __init__(self, errorId, errorTxt):
        self.errorId = errorId
        self.errorTxt = errorTxt


    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)