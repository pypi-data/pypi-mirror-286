 # errorTrace, 
 # errorClassName, 
 # errorFileName, 
 # errorLineNumber, 
 # errorMethodName, 
 # errorMessage, 
 # errorIsError, 
 # errorCode
class HuemulError:
    def __init__(self, org_id, huemul_logging, **args):
        self.errorId = ""
        self.org_id = org_id
        self.error_detail = ""
        self.error_who_is = ""
        self.error_who_code = ""
        self.huemul_logging = huemul_logging

        if (len(args) == 0):
            #val Invoker: Array[StackTraceElement] = new Exception().getStackTrace
            self.error_is_error = False
            self.error_code = ""
            self.error_trace = ""
            self.error_class_name = ""
            self.error_file_name = "" # Invoker(3).getFileName //todo: obtener dinamicamente a partir de los nombres de las clases (descartando)
            self.error_line_number = "" #Invoker(3).getLineNumber
            self.error_method_name = ""
            self.error_message = ""
        elif (len(args) == 4):
            #val Invoker: Array[StackTraceElement] = new Exception().getStackTrace
            self.error_is_error = True
            self.error_code = args["code"] if args["code"] != None else args["error_code"]
            self.error_trace = ""
            self.error_class_name = args["getClassName"] if args["getClassName"] != None else args["error_class_name"]
            self.error_file_name = "" # Invoker(3).getFileName //todo: obtener dinamicamente a partir de los nombres de las clases (descartando)
            self.error_line_number = "" #Invoker(3).getLineNumber
            self.error_method_name = args["getMethodName"] if args["getMethodName"] != None else args["error_method_name"]
            self.error_message = args["message"] if args["message"] != None else args["error_message"]

            self.printError(self.error_message)
        elif len(args) > 4:
            self.error_trace = args["errorTrace"] if args["errorTrace"] != None else args["error_trace"]
            self.error_class_name = args["errorClassName"] if args["errorClassName"] != None else args["error_class_name"]
            self.error_file_name = args["errorFileName"] if args["errorFileName"] != None else args["error_file_name"]
            self.error_line_number = args["errorLineNumber"] if args["errorLineNumber"] != None else args["error_line_number"]
            self.error_method_name = args["errorMethodName"] if args["errorMethodName"] != None else args["error_method_name"]
            self.error_message = args["errorMessage"] if args["errorMessage"] != None else args["error_message"]
            self.error_is_error = args["errorIsError"] if args["errorIsError"] != None else args["error_is_error"]
            self.error_code = args["errorCode"] if args["errorCode"] != None else args["error_code"]

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    # return boolean
    def isOK(self):
        return not (self.error_is_error)

    
    def printError(self, error):
        self.huemul_logging.logMessageError("***************************************************************")
        self.huemul_logging.logMessageError("HuemulLauncher: Error Detail")
        self.huemul_logging.logMessageError("***************************************************************")
        self.huemul_logging.logMessageError("error_ClassName: " + self.error_class_name)
        self.huemul_logging.logMessageError("error_FileName: " + self.error_file_name)
        self.huemul_logging.logMessageError("error_ErrorCode: " + self.error_code)
        self.huemul_logging.logMessageError("error_LineNumber: " + self.error_line_number)
        self.huemul_logging.logMessageError("error_MethodName: " + self.error_method_name)
        self.huemul_logging.logMessageError("error_Message: " + self.error_message)
        self.huemul_logging.logMessageError("error_Trace: " + self.error_trace)

        self.huemul_logging.logMessageError("Detail")
        self.huemul_logging.logMessageError(error)

