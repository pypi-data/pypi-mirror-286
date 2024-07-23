#
# @author Sebastián Rodríguez Robotham
# receive some params
# @param name param name
# @param value param value
#
class HuemulParam:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)