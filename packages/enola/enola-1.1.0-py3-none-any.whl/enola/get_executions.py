from enola.base.common.auth.auth_model import AuthModel
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.connect import Connect
from enola.base.internal.executions.enola_execution import get_execution
from enola.enola_types import Environtment, ExecutionEvalFilter, ExecutionModel, ExecutionQueryModel, TokenInfo

class GetExecutions:
    def __init__(self, token: str, raise_error_if_fail = True):
        """
        Start Executions Execution

        token: jwt token, this is used to identify the agent, request from Admin App
        """
        self.raise_error_if_fail = raise_error_if_fail
        self.num_rows_acum = 0
        self.num_rows = 0
        self.limit = 0
        self.page_number = 0
        self.hf = HuemulFunctions()
        #Connection data

        #get token info
        self.token_info = TokenInfo(token=token)

        if (self.token_info.is_service_account == True and self.token_info.service_account_can_get_executions == False):
            raise Exception("Service Account Token is not allowed to get executions")

        self.connection = Connect(AuthModel(jwt_token=token, url_service=self.token_info.service_account_url_backend, org_id=self.token_info.org_id))

    def get_next_page(self):
        if (self.continue_execution == False):
            raise Exception("No more data to show.")
        
        self.execution_query_model.page_number += 1
        enola_result = self.__run_query()

        #show results
        return enola_result
        

    def get_items(self, 
                 date_from:str,
                 date_to:str,
                 chamber_id_list:list = [], 
                 agent_id_list:list = [], 
                 agent_deploy_id_list:list = [],
                 user_id_list:list = [],
                 session_id_list:list = [],
                 channel_id_list:list = [],
                 data_filter_list:list = [],
                 eval_id_user: ExecutionEvalFilter = None,
                 eval_id_internal: ExecutionEvalFilter = None,
                 eval_id_auto: ExecutionEvalFilter = None,
                 environment_id:Environtment = None,
                 is_test_plan: bool= None,
                 finished:bool = None,
                 limit:int=100, 
                 page_number:int=1, 
                 include_tags:bool=False,
                 include_data:bool=False,
                 include_errors:bool=False,
                 include_evals:bool=False,
                 ) -> ExecutionModel:
        """
        Get Items by Chamber

        date_from: str, date from
        date_to: str, date to
        chamber_id: list, chamber id
        agent_id: list, agent id
        agent_deploy_id: list, agent deploy id
        user_id: list, user id
        session_id: list, session id
        channel_id: list, channel id
        data_filter: list, data filter
        eval_id_user: ExecutionEvalFilter, eval id user
        eval_id_internal: ExecutionEvalFilter, eval id internal
        eval_id_auto: ExecutionEvalFilter, eval id auto
        environment_id: Environtment, environment id
        is_test_plan: bool, is test plan
        finished: bool, finished
        limit: int, limit
        page_number: int, page number
        include_tags: bool, include tags
        include_data: bool, include data
        include_errors: bool, include errors
        include_evals: bool, include evals
        """

        if (self.token_info.agent_deploy_id != None and self.token_info.agent_deploy_id != "" and self.token_info.agent_deploy_id != "0"):
            if (len(agent_deploy_id_list) > 1):
                raise Exception("Service Account Token is not allowed to access more than one agent_deploy_id", self.token_info.agent_deploy_id)
            if (len(agent_deploy_id_list) == 1):
                if (self.token_info.agent_deploy_id != agent_deploy_id_list[0]):
                    raise Exception("Service Account Token is not allowed to access only one agent_deploy_id", self.token_info.agent_deploy_id)
            else:
                agent_deploy_id_list = [self.token_info.agent_deploy_id]


        if (chamber_id_list == [] and agent_id_list == [] and agent_deploy_id_list == []):
            raise Exception("chamber_id or agent_id or agent_deploy_id must be filled.")
    
        self.num_rows_acum = 0
        self.limit = limit
        self.page_number = page_number

        self.execution_query_model = ExecutionQueryModel(
            date_from=date_from,
            date_to=date_to,
            chamber_id_list=chamber_id_list,
            agent_id_list=agent_id_list,
            agent_deploy_id_list=agent_deploy_id_list,
            user_id_list=user_id_list,
            session_id_list=session_id_list,
            channel_id_list=channel_id_list,
            data_filter_list=data_filter_list,
            eval_id_user=eval_id_user,
            eval_id_internal=eval_id_internal,
            eval_id_auto=eval_id_auto,
            environment_id=environment_id,
            is_test_plan=is_test_plan,
            finished=finished,
            limit=limit,
            page_number=page_number,
            include_tags=include_tags,
            include_data=include_data,
            include_errors=include_errors,
            include_evals=include_evals
        )

        enola_result = self.__run_query()

        #show results
        return enola_result
    
    def __run_query(self) -> ExecutionModel:
        """
        Run Query, use self.execution_query_model
        """
        enola_result = get_execution(execution_query_model=self.execution_query_model, connection=self.connection, raise_error_if_fail=self.raise_error_if_fail)

        self.num_rows = len(enola_result.data)
        
        self.continue_execution = False
        if (self.num_rows != self.execution_query_model.limit and self.num_rows != 0):
            self.continue_execution = True

        self.num_rows_acum += self.num_rows

        return enola_result
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
        
