from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.internal.tracking.enola_tracking import create_tracking
from enola.base.common.auth.auth_model import AuthModel
from enola.enola_types import EnolaSenderModel, KindType, DataListModel, DataType, ErrOrWarnKind, Info, Step, StepType, TokenInfo, TrackingModel
from enola.base.connect import Connect


#def add_one(number):
#    return number + 1

class Tracking:
    def __init__(self, token, name, app_id=None, user_id=None, session_id=None, channel_id=None, ip=None, external_id=None, is_test=False, message_input: str = "", enola_id_prev:str = "", app_name:str="", user_name:str="", session_name:str="", channel_name:str="", client_id:str="", product_id:str=""):
        """
        Start tracking Execution

        token: jwt token, this is used to identify the agent, request from Admin App
        name: name of this execution
        message_input: message received from user or to explain the execution
        app_id: id of app, this is used to identify the app who is calling
        user_id: id of external user, this is used to identify the user who is calling
        session_id: id of session of user or application, this is used to identify the session who is calling
        channel_id: web, chat, whatsapp, etc, this is used to identify the channel who is calling
        ip: ip of user or application, this is used to identify the ip who is calling
        external_id: external id, this is used to identify unique records
        is_test: true if this call is for testing purposes
        enola_id_prev: id of previous call, this is used to link agents sequence
        """
        self.name = name
        self.enola_id_prev = enola_id_prev
        self.enola_id = "" #se obtiene al finalizar la ejecución
        self.agent_deploy_id = ""
        self.message_input = message_input
        self.message_output = ""
        self.num_iteratons = 0
        self.hf = HuemulFunctions()
        self.url_evaluation_post = None
        self.url_evaluation_def_get = None

        #this execution information
        self.tracking_status = ""
        #Connection data

        #decodificar jwt
        self.token_info = TokenInfo(token=token)

        if (self.token_info.is_service_account == False):
            raise Exception("This token is not a service account. Only service accounts can execute tracking")

        if not self.token_info.agent_deploy_id:
            raise Exception("agentDeployId is empty.")

        if (self.token_info.service_account_can_tracking == False):
            raise Exception("This service account can't execute tracking")
        

        self.agent_deploy_id = self.token_info.agent_deploy_id
        self.connection = Connect(AuthModel(jwt_token=token, url_service=self.token_info.service_account_url, org_id=self.token_info.org_id))
        
        #user information
        self.enola_sender = EnolaSenderModel(
            app_id=app_id, 
            batch_id=None,
            app_name=app_name, 
            user_id=user_id, 
            user_name=user_name, 
            session_id=session_id, 
            session_name=session_name, 
            channel_id=channel_id, 
            channel_name=channel_name, 
            ip=ip, 
            external_id=external_id, 
            client_id=client_id,
            product_id=product_id,
            )
        
        #if is empty or not exist assign false
        self.is_test = is_test
        
        #save steps and informations
        self.step_list = []
        self.steps = 0
        self.first_step = self.new_step(self.name, message_input= self.message_input)

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

    def add_file_link(self, name: str, url: str, type: str, size_kb: int):
        """
        add file link to tracking
        """
        self.first_step.add_file_link(name=name, url=url, type=type, size_kb=size_kb)

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


    def execute(self, successfull: bool, message_output: str ="", num_iteratons: int = 0, score_value=0, score_group="", score_cluster="", score_date="", external_id="") -> bool:
        """
        register tracking in Enola server
        successfull: true for your Agent execution OK, false for error in your Agent execution
        message_output: message to user or to explain the execution results
        num_iteratons: number of iterations
        score_value: score value
        score_group: score group
        score_cluster: score cluster
        score_date: date of score in ISO & UTC format (example: yyyy-MM-ddTHH:mm:ss:SSSz). Empty for current date
        """
        self.first_step.num_iterations  = num_iteratons
        if (external_id != None and external_id == ""):
            self.enola_sender.external_id = external_id

        self.close_step_others(step=self.first_step, successfull=successfull, others_cost=0, step_id="AGENT", message_output=message_output)
        self.first_step.set_score(value=score_value, group=score_group, cluster=score_cluster, date=score_date)

        #register in server
        print(f'{self.name}: sending to server... ')
        tracking_model = TrackingModel(
            enola_id_prev = self.enola_id_prev,
            enola_sender= self.enola_sender,

            isTest=self.is_test, 
            step_list=self.step_list, 
            steps=self.steps
        )

        #print("paso 10")
        enola_result = create_tracking(tracking_model=tracking_model, connection=self.connection, raise_error_if_fail=True)
        #show results
        if (enola_result.successfull):
            #obtiene url para evaluación
            #obtiene id de enola
            self.enola_id = enola_result.enola_id
            self.agent_deploy_id = enola_result.agent_deploy_id
            self.url_evaluation_post = enola_result.url_evaluation_post
            self.url_evaluation_def_get = enola_result.url_evaluation_def_get

            print(f'{self.name}: finish OK! ')

            return True
        else:
            print(f'{self.name}: finish with error: {enola_result.message}')
            self.tracking_status = enola_result.message

            return False

        


    ########################################################################################
    ###############    S T E P   I N F O     ###############################################
    ########################################################################################


    def new_step(self, name: str, message_input: str = ""):
        """
        start new step
        name: name of this step
        message_input: message received from user or to explain the execution
        """
        #current_step = 
        self.steps += 1
        return Step(name=name, message_input=message_input)

    def close_step_token(self, step: Step, successfull: bool, message_output: str ="", token_input_num: int=0, token_output_num: int=0, token_total_num: int=0, token_input_cost: float=0, token_output_cost: float=0, token_total_cost: float=0, enola_id: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with token information
        enola_id: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id = enola_id
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.TOKEN
        step.token.token_input = token_input_num
        step.token.token_output = token_output_num
        step.token.token_total = token_total_num
        step.cost.token_input = token_input_cost
        step.cost.token_output = token_output_cost
        step.cost.token_total = token_total_cost

        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_video(self, step: Step, successfull: bool, message_output: str ="", video_num: int=0, video_sec: int=0, video_size: int=0, video_cost: float=0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with video information

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.VIDEO
        step.video.num_videos = video_num
        step.video.sec_videos = video_sec
        step.video.size_videos = video_size
        step.cost.videos = video_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)
        
    def close_step_audio(self, step: Step, successfull: bool, message_output: str ="", audio_num:int = 0, audio_sec:int = 0, audio_size:int = 0, audio_cost: float=0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with audio information

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.AUDIO
        step.audio.num_audio = audio_num
        step.audio.sec_audio = audio_sec
        step.audio.size_audio = audio_size
        step.cost.audio = audio_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_image(self, step: Step, successfull: bool, message_output: str ="", image_num:int = 0, image_size:int = 0, image_cost: float = 0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with image information

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.IMAGE
        step.image.num_images = image_num
        step.image.size_images = image_size
        step.cost.images = image_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_doc(self, step: Step, successfull: bool, message_output: str ="", doc_num:int=0, doc_pages:int=0, doc_size:int = 0, doc_char:int=0, doc_cost: float=0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with doc information

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.DOCUMENT
        step.doc.num_docs = doc_num
        step.doc.num_pages = doc_pages
        step.doc.size_docs = doc_size
        step.doc.num_char = doc_char
        step.cost.docs = doc_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)

    def close_step_others(self, step: Step, successfull: bool, message_output: str ="", others_cost: float=0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step with others information

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.OTHER
        step.cost.others = others_cost
        step.date_end = self.hf.get_date_for_api()
        step.duration_in_ms = self.hf.get_dif_ms(step.date_start, step.date_end)
        step.successfull = successfull

        self.step_list.append(step)


    def close_step_score(self, step: Step, successfull: bool, message_output: str ="", others_cost: float=0, enola_id_prev: str="", agent_deploy_id: str="", step_id:str=""):
        """
        close step for Score

        enola_id_prev: If this step was a call to another Enola agent, whether from your own company or another, this is the ID of that agent
        agent_deploy_id: include this if you want to link this step to another agent of another company
        step_id: id of this step, you can use it to link with external calls
        message_output: message to user or to explain the execution results
        """
        step.enola_id_prev = enola_id_prev
        step.agent_deploy_id = agent_deploy_id
        step.step_id = step_id
        step.message_output = message_output
        step.step_type = StepType.SCORE
        step.cost.others = others_cost
        step.successfull = successfull

        self.step_list.append(step)

    

    def __str__(self):
        return f'Agent/Model: {self.name}, Steps: {self.steps}'
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


