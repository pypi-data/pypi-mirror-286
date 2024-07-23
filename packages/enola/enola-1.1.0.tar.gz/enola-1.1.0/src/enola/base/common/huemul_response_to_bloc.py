from ast import Try
import json
import time
from warnings import catch_warnings
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_response_provider import HuemulResponseProvider
from enola.base.connect import Connect

#
# @author Sebastián Rodríguez Robotham
# base class to create, get, getAll methods exposed to user
# @tparam T class Model
#


class HuemulResponseToBloc(HuemulResponseProvider):
    def __init__(self, connect_object: Connect, **args):
        self.data = "" #huemulResponseProvider.dataRaw
        self.connect_object = connect_object
        self.isSuccessful = False
        # status code: 200 OK, 500 error, etc
        self.httpStatusCode = ""
        # text to client
        self.message = "Not started"
        self.startDate = ""
        self.endDate = ""
        self.elapsedTimeMS = -1
        self.transactionId = ""
        # api response version
        self.apiVersion = ""

        #error detail
        self.errors = []
        #data detail
        self.dataRaw = ""
        #extra info detail
        self.extraInfoRaw = ""

        #print("paso 100")
        if (len(args) == 1 and "huemulResponseProvider" in args):
            #print("paso 200")
            self.from_response_provider(args["huemulResponseProvider"])

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


    def from_response_provider(self, huemul_response_provider: HuemulResponseProvider):
        #print("paso 300")
        self.data = huemul_response_provider.data_raw #huemulResponseProvider.dataRaw
        self.isSuccessful = huemul_response_provider.isSuccessful
        # status code: 200 OK, 500 error, etc
        self.httpStatusCode = huemul_response_provider.httpStatusCode
        # text to client
        self.message = huemul_response_provider.message
        self.startDate = huemul_response_provider.startDate
        self.endDate = huemul_response_provider.endDate
        self.elapsedTimeMS = huemul_response_provider.elapsedTimeMS
        self.transactionId = huemul_response_provider.transactionId
        # api response version
        self.apiVersion = huemul_response_provider.apiVersion

        #error detail
        self.errors = huemul_response_provider.errors
        #data detail
        self.dataRaw = huemul_response_provider.data_raw
        #extra info detail
        self.extraInfoRaw = huemul_response_provider.extraInfoRaw
        #print("paso 400")

    #
    #analyze error and determine attempts strategy
    # @param result create/get/getAll response (HuemulResponseBloc type)
    # @param attempt attempt number
    # @return Boolean
    #
    def analyze_errors(self, attempt):
        #print("paso 500")
        continueInLoop = True

        if (self.isSuccessful):
            #all right, exit
            continueInLoop = False
        elif (attempt < self.connect_object.huemul_common.get_total_attempt()):
            #send errors
            self.connect_object.huemul_logging.log_message_info(f"Error in step {self.message}")
            #self.connectObject.huemulLogging.logMessageInfo(str(self.errors))

            try:
                #errorText = ';'.join(map(lambda x: str(x["errorId"]) + ": " + x["errorTxt"],self.errors))
                errorText = self.message if (len(self.errors) == 0) else ';'.join(map(lambda x: str(x["errorId"]) + ": " + x["errorTxt"],self.errors))
            except Exception as e:
                try:
                    #errorText = ';'.join(map(lambda x: str(x.errorId) + ": " + x.errorTxt,self.errors))
                    errorText = self.message if (len(self.errors) == 0) else ';'.join(map(lambda x: str(x.errorId) + ": " + x.errorTxt,self.errors))
                except Exception as e:
                    errorText = "error try to catch error: " + str(e)

            self.connect_object.huemul_logging.log_message_error("errors details: " + errorText)
            self.connect_object.huemul_logging.log_message_error("errors transaction-id: " + self.transactionId)
            #wait from second attempt
            if (attempt > 1):
                # wait 10 seconds and try to call again
                self.connect_object.huemul_logging.log_message_error("waiting 5 seconds.....")
                time.sleep(5)
            

            #get all possible errors
            try:
                connectionError = len(list(filter(lambda x: x.errorId == "APP-101" or x.errorId == "ConnectionError", self.errors)))
            except Exception as e:
                connectionError = len([error for error in self.errors if error.get("errorId") == "APP-101"])
            connectionError = -1 if connectionError == 0 else connectionError

            try:
                unAuthorizedError = len(list(filter(lambda x: x["errorId"] == "2040", self.errors)))
            except Exception as e:
                unAuthorizedError = len([error for error in self.errors if error.get("errorId") == "2040"])
            unAuthorizedError = -1 if unAuthorizedError == 0 else unAuthorizedError

            try:
                forbiddenError = len(list(filter(lambda x: x["errorId"] == "2030", self.errors)))
            except Exception as e:
                forbiddenError = len([error for error in self.errors if error.get("errorId") == "2030"])
            forbiddenError = -1 if forbiddenError == 0 else forbiddenError

            if (forbiddenError > 0):
                self.connect_object.huemul_logging.log_message_error("forbidden")

            if (unAuthorizedError > 0):
                self.connect_object.huemul_logging.log_message_error("attempt " + str(attempt + 1) + " of " + str(self.connect_object.huemul_common.get_total_attempt()))
                #check if error = unauthorized, try to login again
                continueInLoop = True
            elif (connectionError > 0):
                self.connect_object.huemul_logging.log_message_error("attempt " + str(attempt + 1) + " of " + str(self.connect_object.huemul_common.get_total_attempt()))
                #raised error from HuemulConnection method
                continueInLoop = True
            else:
                #unknown error (maybe data), exit and return error
                continueInLoop = False

        else:
            continueInLoop = False


        return continueInLoop
    