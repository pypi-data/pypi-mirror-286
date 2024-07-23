#
# @author Sebastián Rodríguez Robotham
# @param body http return body
# @param httpCode http return code
#
class HuemulHttpInfo:
    def __init__(self, body, httpCode):
        self.body = body
        self.httpCode = httpCode

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)