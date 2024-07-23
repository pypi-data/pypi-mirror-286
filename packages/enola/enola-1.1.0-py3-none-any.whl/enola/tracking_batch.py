from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.tracking_batch.enola_tracking_batch import create_tracking, create_tracking_batch_head
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import EnolaSenderModel, KindType, DataListModel, DataType, ErrOrWarnKind, Info, TokenInfo, TrackingBatchHeadModel, TrackingModel, TrackingResponseModel, Step, StepType
from enola.base.connect import Connect
from typing import List


#def add_one(number):
#    return number + 1

class TrackingBatch:
    def __init__(self, token, name, dataframe, period: str, client_id_column_name:str, product_id_column_name:str, score_value_column_name: str, score_group_column_name, score_cluster_column_name,  app_id=None, app_name:str="",user_id=None, user_name:str="", session_id=None, session_name:str="", channel_id=None, channel_name:str="", ip=None, is_test=False):
        """
        Start tracking Batch Execution

        token: jwt token, this is used to identify the agent, request from Admin App
        name: name of this execution
        dataframe: dataframe to track
        period: period of this execution in iso-format (2021-01-01T00:00:00Z)
        client_id_column_name: name of column with client id
        product_id_column_name: name of column with product id
        score_value_column_name: name of column with score value
        score_group_column_name: name of column with score group
        score_cluster_column_name: name of column with score cluster
        app_id: id of app, this is used to identify the app who is calling
        app_name: name of app, this is used to identify the app who is calling
        user_id: id of external user, this is used to identify the user who is calling
        user_name: name of external user, this is used to identify the user who is calling
        session_id: id of session of user or application, this is used to identify the session who is calling
        session_name: name of session of user or application, this is used to identify the session who is calling
        channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
        channel_name: web, chat, whatsapp, etc, this is used to identify the channel who is calling
        ip: ip of user or application, this is used to identify the ip who is calling
        is_test: true if this call is for testing purposes
        """
        self.name = name
        self.hf = HuemulFunctions()
        self.dataframe = dataframe
        self.client_id_column_name = client_id_column_name
        self.product_id_column_name = product_id_column_name
        self.score_value_column_name = score_value_column_name
        self.score_group_column_name = score_group_column_name
        self.score_cluster_column_name = score_cluster_column_name
        self.period = period


        if (dataframe is None):
            raise Exception("dataframe is empty")
        if (len(dataframe) == 0):
            raise Exception("dataframe is empty (len 0)")
        if (score_value_column_name is None):
            raise Exception("score_value_column_name is empty")
        if (score_value_column_name == ""):
            raise Exception("score_value_column_name is empty")
        if (period is None):
            raise Exception("period is empty")
        if (period == ""):
            raise Exception("period is empty")

        #decodificar jwt
        self.token_info = TokenInfo(token=token)

        if (self.token_info.is_service_account == False):
            raise Exception("This token is not a service account. Only service accounts can execute tracking")

        if not self.token_info.agent_deploy_id:
            raise Exception("agentDeployId is empty.")

        if (self.token_info.service_account_can_tracking == False):
            raise Exception("This service account can't execute tracking")
        

        self.agent_deploy_id = self.token_info.agent_deploy_id
        self.connection = Connect(AuthModel(jwt_token=token, url_service=self.token_info.service_account_url_backend, org_id=self.token_info.org_id))
        
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
            ip=ip, 
            external_id="", 
            batch_id="",
            client_id="",
            product_id="",
            )
        
        #if is empty or not exist assign false
        self.is_test = is_test
        
        #save steps and informations
        self.batch_id = ""

    ########################################################################################
    ###############    A G E N T   M E T H O D S     #######################################
    ########################################################################################


    def add_data_received(self, name:str, data, type:DataType):
        """
        add data received from user
        """
        self.first_step.agent_data_list.append(DataListModel(value=data, name=name, data_type=type, kind=KindType.RECEIVER)) 

    def add_data_send(self, name:str, data, type:DataType):
        """
        add data to send to user
        """
        self.first_step.agent_data_list.append(DataListModel(value=data, name=name, data_type=type, kind=KindType.SENDER)) 
        
    def add_custom_info(self, key, value):
        """
        add custom information to tracking
        """
        self.first_step.info_list.append(Info(key, value))

    def add_tag(self, key: str, value):
        """
        add tag to tracking, this tag is used to search in Enola App
        """
        self.first_step.add_tag(key=key, value=value)

    def add_extra_info(self, key: str, value):
        """
        add extra information to tracking, this can be used to test or debug
        """
        self.first_step.add_extra_info(key=key, value=value)

    def add_error(self, id: str, message: str, kind: ErrOrWarnKind):
        """
        register error to tracking
        """
        self.first_step.add_error(id=id, message=message, kind=kind)

    def add_warning(self, id: str, message: str, kind: ErrOrWarnKind):
        """
        register warning to tracking
        """
        self.first_step.add_warning(id=id, message=message, kind=kind)


    def execute(self, batch_size=200) -> List[TrackingResponseModel]:
        """
        register tracking batch in Enola server
        """

        #create batch
        if (self.batch_id == ""):
            print(f'{self.name}: sending to server, create Batch... ')
            tracking_batch_model = TrackingBatchHeadModel(
                enola_sender=self.enola_sender, 
                period=self.period,
                total_rows=len(self.dataframe),
                name=self.name, 
                is_test=self.is_test)
            
            tracking_batch = create_tracking_batch_head(tracking_batch_model=tracking_batch_model, connection=self.connection, raise_error_if_fail=False)
            self.batch_id = tracking_batch.batch_id
            self.enola_sender.batch_id = self.batch_id

        #start cycle to send all data
        print(f'{self.name}: sending to server, upload... ')
        #show results
        if (self.batch_id == ""):
            print(f'{self.name}: finish with error, batch_id is empty')
            return []
        
        totalRows = len(self.dataframe)
        listToSend = []
        resultsList = []
        #recorrer la lista
        for (index, row) in self.dataframe.iterrows():

            #create step
            step = Step(
                    name="Prediction",
                    message_input="",
                )
            
            #add data to step in extra info
            for column in self.dataframe.columns:
                step.add_extra_info(column, row[column])

            if (self.score_cluster_column_name in self.dataframe.columns):
                step.score_cluster = row[self.score_cluster_column_name]
            if (self.score_group_column_name in self.dataframe.columns):
                step.score_group = row[self.score_group_column_name]
            if (self.score_value_column_name in self.dataframe.columns):
                step.score_value = row[self.score_value_column_name]
            if (self.client_id_column_name in self.dataframe.columns):
                step.client_id = row[self.client_id_column_name]
            if (self.product_id_column_name in self.dataframe.columns):
                step.product_id = row[self.product_id_column_name]
            
            step.step_type = StepType.SCORE
            step.successfull = True
            step.set_score(
                value=step.score_value, 
                group=step.score_group, 
                cluster=step.score_cluster, 
                date=step.date_start
                )

            #crear registro con el mismo metodo del real-time
            tracking_model = TrackingModel(
                isTest=self.is_test,
                enola_sender=self.enola_sender,
                enola_id_prev="",
                steps=1,
                step_list=[step]
            )

            #add to list
            listToSend.append(tracking_model)

            #agregarlo al arreglo de envio
            if (len(listToSend) == batch_size or index == totalRows-1):
                #send to enola
                tracking_batch = create_tracking (tracking_list_model=listToSend, connection=self.connection, raise_error_if_fail=False)

                if (tracking_batch.successfull == False):
                    print(f'{self.name}: finish with error, batch_id is empty')
                    return []
                
                resultsList.extend(tracking_batch.tracking_list)
                self.connection.huemul_logging.log_message_info(message = f"sending {len(resultsList)} of {totalRows}...")

                #clean and continue
                listToSend = []



        self.connection.huemul_logging.log_message_info(message = f'{self.name}: finish OK! ')
        self.connection.huemul_logging.log_message_info(message = f"finish OK with batch_id: {self.batch_id}")

        return resultsList
        

        #finish OK
        
        



    def __str__(self):
        return f'Agent/Model: {self.name}, Steps: {self.steps}'
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


