import logging

class HuemulLogging:
    def __init__(self):
        FORMAT = '%(asctime)s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.logger = logging.getLogger('Enola')

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    #
    # logMessageDebug: Send {message} to log4j - Debug
    #
    def logMessageDebug(self, message):
        self.logger.debug(message)

    #
    # logMessageInfo: Send {message} to log4j - Info
    #
    def log_message_info(self, message):
        self.logger.info(message)

    #
    # logMessageWarn: Send {message} to log4j - Warning
    #
    def logMessageWarn(self, message):
        self.logger.warn(message)

    #
    # logMessageError: Send {message} to log4j - Error
    #
    def log_message_error(self, message):
        self.logger.error(msg = str(message), extra={"error": message})