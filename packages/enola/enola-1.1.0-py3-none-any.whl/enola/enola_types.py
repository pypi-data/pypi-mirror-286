from enola.base.common.huemul_functions import HuemulFunctions
from enum import Enum
import json
import jwt
from typing import List

class Environtment(Enum):
    DEV = "DEV"
    QA = "QA"
    PROD = "PROD"

class DataType(Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"

class CompareType(Enum):
    EQUAL = "EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    CONTAINS = "CONTAINS"

class TokenInfo:
    def __init__(self, token: str):

        if token == "":
                raise Exception("token is empty.")
        
        try:
            decoded = jwt.decode(token, algorithms=['none'], options={'verify_signature': False})
            self.agent_deploy_id = decoded.get("agentDeployId", None)
            self.org_id = decoded.get("orgId", None)
            self.service_account_id = decoded.get("id", None)
            self.service_account_name = decoded.get("displayName", None)
            self.service_account_url = decoded.get("url", None)
            self.service_account_url_backend = decoded.get("urlBackend", None)
            self.service_account_can_tracking = decoded.get("canTracking", False)
            self.service_account_can_evaluate = decoded.get("canEvaluate", False)
            self.is_service_account = decoded.get("isServiceAccount", False)
            self.service_account_can_get_executions = decoded.get("canGetExecutions", False)

            #verify if serviceAccountUrl is empty, return error
            if not self.service_account_url:
                raise Exception("serviceAccountUrl is empty.")
            if not self.service_account_url_backend:
                raise Exception("serviceAccountUrlBackend is empty.")
            if not self.org_id:
                raise Exception("orgId is empty.")
            
        except jwt.ExpiredSignatureError:
            print("token expired.")
        except jwt.DecodeError:
            print("Error decoding token.")
        except jwt.InvalidTokenError:
            print("Invalid Token.")


    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class KindType(Enum):
    RECEIVER = "RECEIVER"
    SENDER = "SENDER"

class ErrorType(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"

class ErrOrWarnKind(Enum):
    """
    EXTERNAL: external agent call generate an unexpected error or warning
    """
    EXTERNAL = "EXTERNAL"
    """
    INTERNAL_CONTROLLED: internal agent call generate an unexpected error or warning
    """
    INTERNAL_CONTROLLED = "INTERNAL_CONTROLLED"
    """
    INTERNAL_TOUSER: controlled error or warning to send to user
    """
    INTERNAL_TOUSER = "INTERNAL_TOUSER"

class ErrorOrWarnModel:
    def __init__(self, id: str, message: str, error_type: ErrorType, kind: ErrOrWarnKind):
        self.id = id
        self.error = message
        self.error_type: ErrorType = error_type
        self.kind: ErrOrWarnKind = kind

    def to_json(self):
        return {
            "id": self.id,
            "error": self.error,
            "error_type": self.error_type.value,
            "kind": self.kind.value
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class DataListModel:
    def __init__(self, kind: KindType, name: str, data_type: DataType, value):
        self.kind = kind
        self.name = name
        self.data_type = data_type
        self.value = value

    def to_json(self):
        return {
            "kind": self.kind.value,
            "name": self.name,
            "data_type": self.data_type.value,
            "value": self.value
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class Info:

    def is_numeric(self, value):
        return isinstance(value, (int, float, complex))
    def is_string(self, value):
        return isinstance(value, (str))
    def is_dict(self, value):
        return isinstance(value, (dict))

    def __init__(self, type: str, key: str, value):
        self.type = type
        self.key = key
        #si valor es numerico, asignar
        if (self.is_numeric(value)):
            self.value = value
        elif (self.is_string(value)):
            if (self.is_dict(value)):
                self.value = json.dumps(value)
            else:
                self.value = value
        else:
            self.value = value
        

    def to_json(self):
        return {
            "type": self.type,
            "key": self.key,
            "value": self.value
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class ApiDataModel:
    def __init__(self, name: str, method: str, url: str, body: str, header: str, payload: str, description: str):
        self.name = name
        self.method = method
        self.url = url
        self.description = description
        self.body = body
        self.header = header
        self.payload = payload


    def to_json(self):
        return {
            "name": self.name,
            "method": self.method,
            "url": self.url,
            "description": self.description,
            "body": self.body,
            "header": self.header,
            "payload": self.payload
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class FileInfoModel:
    def __init__(self, name: str, url: str, type: str, sizeKb: int, description: str):
        self.name = name
        self.url = url
        self.type = type
        self.size = sizeKb
        self.description = description

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "type": self.type,
            "size": self.size,
            "description": self.description
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class EnolaSenderModel:
    """
    EnolaSenderModel
    """
    def __init__ (self, 
                app_id: str, 
                app_name: str, 
                user_id: str, 
                user_name: str, 
                session_id: str, 
                session_name: str, 
                channel_id: str, 
                channel_name: str, 
                client_id: str,
                product_id: str,
                external_id: str,
                batch_id: str,
                  ip: str):
        self.app_id=app_id
        self.app_name=app_name
        self.user_id=user_id
        self.user_name=user_name
        self.session_id=session_id
        self.session_name=session_name
        self.channel_id=channel_id
        self.channel_name=channel_name
        self.client_id=client_id
        self.product_id=product_id
        self.external_id=external_id
        self.batch_id=batch_id
        self.ip=ip

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)



#***********************************************************************************
#*************   S T E P S    T Y P E S     ***********************************
#***********************************************************************************

class StepCost:
    def __init__(self):
        self.token_input = 0
        self.token_output = 0
        self.token_total = 0
        self.videos = 0
        self.audio = 0
        self.images = 0
        self.docs = 0
        self.infra = 0
        self.others = 0
        self.total = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class StepVideo:
    def __init__(self):
        self.num_videos = 0
        self.size_videos = 0
        self.sec_videos = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class StepAudio:
    def __init__(self):
        self.size_audio = 0
        self.num_audio = 0
        self.sec_audio = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class StepImage:
    def __init__(self):
        self.num_images = 0
        self.size_images = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class StepDoc:
    def __init__(self):
        self.num_docs = 0
        self.num_pages = 0
        self.size_docs = 0
        self.num_char = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class StepToken:
    def __init__(self):
        self.num_char = 0
        self.token_input = 0
        self.token_output = 0
        self.token_total = 0

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class StepType(Enum):
    TOKEN = "TOKEN"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"
    DOCUMENT = "DOCUMENT"
    OTHER = "OTHER"
    SCORE = "SCORE"

class Step:
    def __init__(self, name: str, message_input: str = ""):
        self.hf = HuemulFunctions()
        self.name = name
        self.enola_id = ""
        self.agent_deploy_id = ""
        self.step_id = ""
        self.message_input = message_input
        self.message_output = ""
        self.num_iterations = 0
        self.step_id_prev = ""
        self.date_start = self.hf.get_date_for_api()
        self.date_end = self.date_start
        #self.result_list = []
        self.agent_data_list = [] #only for first step
        self.errOrWarn_list = []
        self.extra_info_list = []
        self.file_info_list = []
        self.step_api_data_list = []
        self.step_type:StepType = StepType.OTHER

        self.successfull = False
        self.num_errors = 0
        self.num_warnings = 0

        self.score_value=0
        self.score_group=""
        self.score_cluster=""

        self.video = StepVideo()
        self.audio = StepAudio()
        self.image = StepImage()
        self.doc = StepDoc()
        self.token = StepToken()
        self.cost = StepCost()
        self.income_total = 0
        self.duration_in_ms = 0

    def set_score(self, value: int, group: str, cluster: str, date: str = ""):
        """
        Set score for step
        value: score value
        group: score group
        cluster: score cluster
        date: date of score in ISO & UTC format (example: yyyy-MM-ddTHH:mm:ss:SSSz). Empty for current date
        """
        self.score_value = value
        self.score_group = group
        self.score_cluster = cluster
        if (date != ""):
            self.date_start = date
            self.date_end = date


    def add_api_data(self, bodyToSend: str, payloadReceived: str, name: str, method: str, url: str, description: str = "", headerToSend: str = ""):
        self.step_api_data_list.append(ApiDataModel(name=name, method=method, url=url, body=bodyToSend, header=headerToSend, payload=payloadReceived, description=description)) 
        #{"body": bodyToSend, "header": headerToSend, "payload": payloadReceived})

    def add_file_link(self, name: str, url: str, type: str, size_kb: int, description: str = ""):
        self.file_info_list.append(FileInfoModel(name=name, url=url, type=type, sizeKb=size_kb, description=description))
        #{"name": name, "url": url, "type": type, "size": size})

    def add_tag(self, key: str, value):
        self.extra_info_list.append(Info(type="tag", key=key, value=value))
        
    def add_extra_info(self, key: str, value):
        self.extra_info_list.append(Info(type="info", key=key, value=value))

    def add_error(self, id: str, message: str, kind: ErrOrWarnKind):
        self.num_errors += 1
        self.errOrWarn_list.append(ErrorOrWarnModel(id=id, message=message, error_type=ErrorType.ERROR, kind=kind))

    def add_warning(self, id: str, message: str, kind: ErrOrWarnKind):
        self.num_warnings += 1
        self.errOrWarn_list.append(ErrorOrWarnModel(id=id, message=message, error_type=ErrorType.ERROR, kind=kind))

    def to_json(self):
        return {
            "stepId": self.step_id,
            "stepIdPrev": self.step_id_prev,
            "stepDateStart": self.date_start,
            "stepDateEnd": self.date_end,
            "agentDeployId": self.agent_deploy_id,
            "agentExecName": self.name,
            "agentExecDurationMs": self.duration_in_ms,
            "agentExecSuccessfull": self.successfull,
            "agentExecNumErrors": self.num_errors,
            "agentExecNumWarnings": self.num_warnings,
            "agentExecNumVideos": self.video.num_videos,
            "agentExecSecVideos": self.video.sec_videos,
            "agentExecSizeAudio": self.video.size_videos,
            "agentExecNumAudio": self.audio.num_audio,
            "agentExecSecAudio": self.audio.sec_audio,
            "agentExecSizeVideos": self.video.size_videos,
            "agentExecNumImages": self.image.num_images,
            "agentExecSizeImages": self.image.size_images,
            "agentExecNumDocs": self.doc.num_docs,
            "agentExecNumPages": self.doc.num_pages,
            "agentExecSizeDocs": self.doc.size_docs,
            "agentExecNumChar": self.doc.num_char + self.token.num_char,
            "agentExecTokenInput": self.token.token_input,
            "agentExecTokenOutput": self.token.token_output,
            "agentExecTokenTotal": self.token.token_total,
            "agentExecCostTokenInput": self.cost.token_input,
            "agentExecCostTokenOutput": self.cost.token_output,
            "agentExecCostTokenTotal": self.cost.token_total,
            "agentExecCostVideos": self.cost.videos,
            "agentExecCostAudio": self.cost.audio,
            "agentExecCostImages": self.cost.images,
            "agentExecCostDocs": self.cost.docs,
            "agentExecCostInfra": self.cost.infra,
            "agentExecCostOthers": self.cost.others,
            "agentExecCostTotal": self.cost.total,
            "agentExecIncomeTotal": self.income_total,
            "agentExecScoreValue": self.score_value,
            "agentExecScoreGroup": self.score_group,
            "agentExecScoreCluster": self.score_cluster,
            "agentExecType": self.step_type.value,

            "agentExecMessageInput": self.message_input,
            "agentExecMessageOutput": self.message_output,
            "agentExecCliNumIter": self.num_iterations,

            "agentData": list(map(lambda x: x.to_json(), self.agent_data_list)),
            "errorOrWarning": list(map(lambda x: x.to_json(), self.errOrWarn_list)),
            "extraInfo": list(map(lambda x: x.to_json(), self.extra_info_list)),
            "fileInfo": list(map(lambda x: x.to_json(), self.file_info_list)),
            "stepApiData": list(map(lambda x: x.to_json(), self.step_api_data_list)),
        }

    def __str__(self):
        return f'Step: {self.description}, Duration: {self.duration} seconds'
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


#***********************************************************************************
#*************   T R A C K I N G   T Y P E S     ***********************************
#***********************************************************************************

class TrackingModel:
    """
    TrackingModel
    """
    def __init__(self, isTest: bool, step_list: List[Step], steps: int, enola_id_prev: str, enola_sender: EnolaSenderModel):
        self.enola_sender = enola_sender
        
        self.isTest = isTest
        #step_list es una lista, generar un arreglo ejecutando el metodo to_json de cada elemento de la lista con map
        self.step_list = step_list
        self.steps = steps
        self.enola_id_prev = enola_id_prev

    def to_json(self):
        return {
            "app_id": self.enola_sender.app_id,
            "app_name": self.enola_sender.app_name,
            "user_id": self.enola_sender.user_id,
            "user_name": self.enola_sender.user_name,
            "session_id": self.enola_sender.session_id,
            "channel_id": self.enola_sender.channel_id,
            "session_name": self.enola_sender.session_name,
            "client_id": self.enola_sender.client_id,
            "product_id": self.enola_sender.product_id,
            "agentExecBatchId": self.enola_sender.batch_id,
            "ip": self.enola_sender.ip,
            "code_api": self.enola_sender.external_id,
            "isTest": self.isTest,
            "step_list": list(map(lambda x: x.to_json(), self.step_list)),
            "steps": self.steps,
            "enola_id_prev": self.enola_id_prev
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class TrackingResponseModel:
    def __init__(self, successfull: bool = None, enola_id: str="", agent_deploy_id:str="", message: str="", url_evaluation_def_get: str="", url_evaluation_post: str="",  **args):
        self.enola_id = enola_id if enola_id != "" else args.get("agentExecuteId", "")
        self.agent_deploy_id = agent_deploy_id if agent_deploy_id != "" else args.get("agentDeployId", "")
        self.url_evaluation_def_get = url_evaluation_def_get if url_evaluation_def_get != "" else args.get("urlEvaluationDefGet", "")
        self.url_evaluation_post = url_evaluation_post if url_evaluation_post != "" else args.get("urlEvaluationPost", "")
        self.successfull = successfull if successfull != "" and successfull != None else args.get("isSuccessful", False)
        self.message = message if message != "" else args.get("message", "")
        self.args = args

    def to_json(self):
        return {
            "enolaId": self.enola_id,
            "agentDeployId": self.agent_deploy_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

#***********************************************************************************
#*************   T R A C K I N G   B A T C H   T Y P E S     ***********************
#***********************************************************************************

class TrackingBatchHeadModel:
    """
    TrackingBatchHeadModel
    """
    def __init__(self, name: str, period: str, total_rows: int, is_test: bool, enola_sender: EnolaSenderModel):
        self.enola_sender = enola_sender
        self.name = name
        self.period = period
        self.total_rows = total_rows
        self.is_test = is_test

    def to_json(self):
        return {
            "agentExecBatchCliAppId": self.enola_sender.app_id,
            "agentExecBatchCliAppName": self.enola_sender.app_name,
            "agentExecBatchCliUserId": self.enola_sender.user_id,
            "agentExecBatchCliUserName": self.enola_sender.user_name,
            "agentExecBatchCliSessionId": self.enola_sender.session_id,
            "agentExecBatchCliChannel": self.enola_sender.channel_id,
            "agentExecBatchCliChannelName": self.enola_sender.channel_name,
            "agentExecBatchCliSessionName": self.enola_sender.session_name,
            "agentExecBatchCliIP": self.enola_sender.ip,
            "agentExecBatchName": self.name,
            "agentExecBatchPeriodData": self.period,
            "agentExecBatchIsTest": self.is_test,
            "agentExecBatchNumRowsTotal": self.total_rows
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class TrackingBatchHeadResponseModel:
    def __init__(self, batch_id: str, agent_deploy_id:str, successfull: bool, message: str,  **args):
        self.batch_id = batch_id
        self.agent_deploy_id = agent_deploy_id
        self.successfull = successfull
        self.message = message
        self.args = args

    def to_json(self):
        return {
            "batch_id": self.batch_id,
            "agentDeployId": self.agent_deploy_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class TrackingBatchDetailResponseModel:
    def __init__(self, agent_deploy_id:str="", successfull: bool = None, message: str = "", tracking_list: List[TrackingResponseModel] = [], **args):
        #self.tracking_list = tracking_list if tracking_list != "" and len(tracking_list) > 0 else args.get("trackingList", [])
        self.tracking_list: List[TrackingResponseModel] = [] if len(tracking_list) == 0 else list(map(lambda x: TrackingResponseModel(**x) ,tracking_list))
        if (len(self.tracking_list) == 0 and len(args.get("trackingList", [])) > 0):
            self.tracking_list = list(map(lambda x: TrackingResponseModel(**x) ,args.get("trackingList", [])))
        self.agent_deploy_id = agent_deploy_id if agent_deploy_id != "" else args.get("agentDeployId", "")
        self.successfull = successfull if successfull != "" and successfull != None else args.get("isSuccessful", False)
        self.message = message if message != "" else args.get("message", "")
        self.args = args
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

#***********************************************************************************
#*************   E X E C U T I O N   T Y P E S     ***********************************
#***********************************************************************************

class ExecutionModel:
    def __init__(self, data: list, successfull: bool, message: str, **args):
        self.data = data
        self.successfull = successfull
        self.message = message
        self.args = args

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class ExecutionEvalFilter:
    def __init__(self, eval_id: list, include: bool = True):
        self.eval_id = eval_id
        self.include = include

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class ExecutionDataFilter:
    def __init__(self, name: str, value, type: DataType = DataType.TEXT, compare: CompareType = CompareType.EQUAL):
        self.name = name
        self.value = value
        self.type = type
        self.compare = compare

    def to_json(self):
        return {
            "name": self.name,
            "value": self.value,
            "type": self.type.value,
            "compare": self.compare.value
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
class ExecutionQueryModel:
    def __init__(self,
        date_from:str,
        date_to:str,
        chamber_id_list:list = [], 
        agent_id_list:list = [], 
        agent_deploy_id_list:list = [],
        user_id_list:list = [],
        session_id_list:list = [],
        channel_id_list:list = [],
        data_filter_list:list = [], #ExecutionDataFilter
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
        include_evals:bool=False):
        self.date_from = date_from
        self.date_to = date_to
        self.chamber_id_list = chamber_id_list
        self.agent_id_list = agent_id_list
        self.agent_deploy_id_list = agent_deploy_id_list
        self.user_id_list = user_id_list
        self.session_id_list = session_id_list
        self.channel_id_list = channel_id_list
        self.data_filter_list = data_filter_list
        self.eval_id_user = eval_id_user
        self.eval_id_internal = eval_id_internal
        self.eval_id_auto = eval_id_auto
        self.environment_id = environment_id
        self.isTestPlan = is_test_plan
        self.finished = finished
        self.limit = limit
        self.page_number = page_number
        self.includeTags = include_tags
        self.includeData = include_data
        self.includeErrors = include_errors
        self.includeEvals = include_evals

        if (date_from == ""):
            raise Exception("date_from is empty.")
        if (date_to == ""):
            raise Exception("date_to is empty.")
        if (limit == 0):
            raise Exception("limit is 0.")
        if (page_number == 0):
            raise Exception("page is 0.")
        if (limit < 1):
            raise Exception("limit must be greater than 0.")
        if (page_number < 1):
            raise Exception("page_number must be greater than 0.")
        
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
        
class ExecutionResponseModel:
    def __init__(self,
                agentExecId: str,
                agentExecIdRelated: str,
                agentDeployId: str,
                agentDeployName: str,
                agentId: str,
                agentName: str,
                agentExecName: str,
                agentExecStartDT: str,
                agentExecEndDT: str,
                agentExecDurationMs: int,
                agentExecNumTracking: str,
                agentExecIsTest: bool,
                environmentId: str,

                agentExecCliAppId: str,
                agentExecCliAppName: str,
                agentExecCliUserId: str,
                agentExecCliUserName: str,
                agentExecCliSessionId: str,
                agentExecCliSessionName: str,
                agentExecCliChannel: str,
                agentExecCliChannelName: str,
                agentExecMessageInput : str,
                agentExecMessageOutput : str,
                agentExecTagJson : json,
                agentExecFileInfoJson : json,
                agentExecDataJson : json,
                agentExecErrorOrWarningJson : json,
                agentExecStepApiDataJson : json,
                agentExecInfoJson : json,
                agentExecEvals: json,
                agentExecCliIP: str,
                agentExecCliNumIter: int,
                agentExecCliCodeApi: str,
                agentExecSuccessfull: bool,
                **args
                 ):
        self.enola_id = agentExecId
        self.enola_id_related = agentExecIdRelated
        self.agent_deploy_id = agentDeployId
        self.agent_deploy_name = agentDeployName
        self.agent_id = agentId
        self.agent_name = agentName
        self.name = agentExecName
        self.start_dt = agentExecStartDT
        self.end_dt = agentExecEndDT
        self.duration_ms = agentExecDurationMs
        self.num_tracking = agentExecNumTracking
        self.is_test = agentExecIsTest
        self.environment_id = environmentId
        self.app_id = agentExecCliAppId
        self.app_name = agentExecCliAppName
        self.user_id = agentExecCliUserId
        self.user_name = agentExecCliUserName
        self.session_id = agentExecCliSessionId
        self.session_name = agentExecCliSessionName
        self.channel = agentExecCliChannel
        self.channel_name = agentExecCliChannelName
        self.message_input = agentExecMessageInput
        self.message_output = agentExecMessageOutput
        self.tag_json = agentExecTagJson
        self.file_info_json = agentExecFileInfoJson
        self.data_json = agentExecDataJson
        self.error_or_warning_json = agentExecErrorOrWarningJson
        self.step_api_data_json = agentExecStepApiDataJson
        self.info_json = agentExecInfoJson
        self.evals = agentExecEvals
        self.ip = agentExecCliIP
        self.num_iter = agentExecCliNumIter
        self.external_id = agentExecCliCodeApi
        self.successfull = agentExecSuccessfull

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

#***********************************************************************************
#*************   E V A L U A T I O N   T Y P E S     ***********************************
#***********************************************************************************

class EvaluationResultModel:
    def __init__(self, total_evals: int, total_errors: int, total_success: int, errors: list):
        self.total_evals = total_evals
        self.total_errors = total_errors
        self.total_success = total_success
        self.errors = errors

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class EvaluationDetailModel:
    """
    EvaluationDetailModel
    """
    def __init__(self, eval_id: str, value: float, comment: str):
        self.eval_id = eval_id
        self.value = value
        self.comment = comment

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class EvaluationModel:
    """
    EvaluationModel
    """
    def __init__(self, enola_id: str, enola_sender: EnolaSenderModel):
        self.enola_id = enola_id
        self.evals = []
        self.enola_sender = enola_sender

    def add_eval(self, eval: EvaluationDetailModel):
        self.evals.append(eval)

    def to_json(self):
        result = {
            "enolaId": self.enola_id,
            "evalType": "AUTO",
            "sender": {
                "app_id": self.enola_sender.app_id,
                "app_name": self.enola_sender.app_name,
                "user_id": self.enola_sender.user_id,
                "user_name": self.enola_sender.user_name,
                "session_id": self.enola_sender.session_id,
                "session_name": self.enola_sender.session_name,
                "channel_id": self.enola_sender.channel_id,
                "channel_name": self.enola_sender.channel_name,
                "ip": self.enola_sender.ip
            },
            "evals": {
                item.eval_id: {
                    "value": item.value,
                    "comment": item.comment
                }
                for item in self.evals
            }
        }
        return result;

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

class EvaluationResponseModel:
    def __init__(self, enola_id: str="", agent_deploy_id:str="", enola_eval_id: str="", successfull: bool=True, message: str = "",  **args):
        self.enola_id = enola_id if enola_id != "" else args.get("enolaId", None)
        self.agent_deploy_id = agent_deploy_id if agent_deploy_id != "" else args.get("agentDeployId", None)
        self.enola_eval_id = enola_eval_id if enola_eval_id != "" else args.get("enolaEvalId", None)
        self.successfull = successfull if successfull != "" else args.get("IsSuccessfull", None)
        self.message = message
        self.args = args

    def to_json(self):
        return {
            "enolaId": self.enola_id,
            "agentDeployId": self.agent_deploy_id,
            "enolaEvalId": self.enola_eval_id,
            "successfull": self.successfull,
            "message": self.message,
            "args": self.args
        }
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

