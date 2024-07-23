import jwt
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.evaluation.enola_evaluation import create_evaluation
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import EnolaSenderModel, EvaluationDetailModel, EvaluationModel, EvaluationResultModel, TokenInfo
from enola.base.connect import Connect


class Evaluation:
    def __init__(self, token, app_id=None, user_id=None, session_id=None, channel_id=None, ip=None, app_name:str="", user_name:str="", session_name:str="", channel_name:str=""):
        """
        Start Evaluation Execution

        token: jwt token, this is used to identify the agent, request from Admin App
        app_id: id of app, this is used to identify the app who is calling
        app_name: name of app, this is used to identify the app who is calling
        user_id: id of external user, this is used to identify the user who is calling
        user_name: name of external user, this is used to identify the user who is calling
        session_id: id of session of user or application, this is used to identify the session who is calling
        channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
        channel_name: web, chat, whatsapp, etc, this is used to identify the channel who is calling
        ip: ip of user or application, this is used to identify the ip who is calling
        """
        self.hf = HuemulFunctions()
        #Connection data

        #decodificar jwt
        self.token_info = TokenInfo(token=token)

        if (self.token_info.is_service_account == False):
            raise Exception("This token is not a service account. Only service accounts can execute evaluations.")

        if (self.token_info.is_service_account == True and self.token_info.service_account_can_evaluate == False):
            raise Exception("Service Account can't evaluate")


        self.connection = Connect(AuthModel(jwt_token=token, url_service=self.token_info.service_account_url, org_id=self.token_info.org_id))
        

        #user information
        self.enola_sender = EnolaSenderModel(
            app_id=app_id, 
            app_name=app_name, 
            user_id=user_id, 
            user_name=user_name, 
            session_id=session_id, 
            session_name=session_name, 
            channel_id=channel_id, 
            channel_name=channel_name, 
            batch_id="",
            client_id="",
            external_id="",
            product_id="",
            ip=ip
            )

        #current date
        self.date_start = self.hf.get_date_for_api()
        self.executions = []
                
        #save steps and informations

    ########################################################################################
    ###############    E V A L U A T I O N     M E T H O D S     ###########################
    ########################################################################################


    def execution_exists(self, enola_id: str):
        """
        Check if execution exists
        enola_id: id of enola
        """
        for item in self.executions:
            if item.enola_id == enola_id:
                return item
        return None

    def add_evaluation(self, enola_id: str, eval_id: str, value: float, comment: str):
        """
        Add Evaluation
        enola_id: id of enola
        eval_id: id of evaluation
        value: value of evaluation
        comment: comment of evaluation
        """

        eval = EvaluationDetailModel(eval_id, value, comment)
        #check if enola_id exists (append eval), if not, create new enola_id
        execution = self.execution_exists(enola_id)


        if (execution is None):
            execution = EvaluationModel(enola_id, enola_sender = self.enola_sender)
            self.executions.append(execution)
        
        execution.add_eval(eval)

    def execute(self):
        """
        Execute Evaluations
        """
        final_result: EvaluationResultModel = EvaluationResultModel(
            total_evals=len(self.executions), 
            total_errors=0, 
            total_success=0, 
            errors=[]
        )
        
        for item in self.executions:
            result = create_evaluation(evaluation_model=item, connection=self.connection)
            if not result.successfull:
                print(result.errors)
                print(result.message)
                final_result.errors.append(result.message)

        return final_result
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

