from enola.base.common.auth.auth_model import AuthModel
from enola.base.common.huemul_common import HuemulCommon
from enola.base.common.huemul_error import HuemulError
from enola.base.common.huemul_logging import HuemulLogging

# authData: AuthModel
class Connect:
    def __init__(self, auth_data: AuthModel):
        self.authData = auth_data
        self.huemul_logging = HuemulLogging()
        self.huemul_logging.log_message_info(message = "WELCOME to Enola...")

        self._can_execute = False
        self._is_open = True
        self._error_message = ""
        self.others_params = []
        self.control_class_name = "" #: String = Invoker(1).getClassName.replace("$", "")
        self.control_method_name = "" #: String = Invoker(1).getMethodName.replace("$", "")
        #val controlFileName: String = Invoker(1).getFileName.replace("$", "")

        #create error and common object
        self.control_error = HuemulError(org_id=auth_data.org_id, huemul_logging=self.huemul_logging)
        self.huemul_common = HuemulCommon()
        
        #valida que jwtToken no sea nulo
        if (auth_data.jwt_token is None):
            self.huemul_logging.log_message_error(message = "jwtToken is null")
            self._error_message = "jwtToken is null"
            self._is_open = False
            return

        #store credentials and token
        self.huemul_common.set_org_id(auth_data.org_id)
        self.huemul_common.set_consumer_id(auth_data.consumer_id)
        self.huemul_common.set_consumer_secret(auth_data.consumer_secret)
        self.huemul_common.set_application_name(auth_data.application_name)
        self.huemul_common.set_jwt_token(auth_data.jwt_token)
        self.huemul_common.set_token_id(self.authData.jwt_token)
        self.huemul_common.set_service_url(self.authData.url_service)
        

        self.huemul_logging.log_message_info(message = "authorized...")
        self.can_execute = True
        self.huemul_logging.log_message_info(message = "STARTED!!!")

        ### END START
        
    def is_open(self):
        return self._is_open

    #/************************************************************************************/
    #/******************  R E S U L T S    ***********************************************/
    #/************************************************************************************

    
    

    #/************************************************************************************/
    #/******************  U T I L   F U N C T I O N S    *********************************/
    #/************************************************************************************/

    #
    # true for execute, false can't execute
    # @return
    #
    def can_execute(self):
        return self._can_execute

    #
    # return error message
    # @return
    #
    def get_error_message(self):
        return self._error_message
    
    