import base64
import json
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.common.huemul_response_error import HuemulResponseError
from enola.base.common.huemul_response_to_bloc import HuemulResponseToBloc
from enola.enola_types import ExecutionQueryModel, ExecutionResponseModel

class EnolaExecutionProvider(HuemulResponseToBloc):
    
    #
    # execution_get
    # @param ExecutionModel executionModel
    # @return AgentExecuteResponseModel[AgentExecuteResponseModel]
    #
    def execution_get(self, execution_query_model: ExecutionQueryModel):
        #self = AgentExecuteResponseModel()
        try:
            hf = HuemulFunctions()
            excludeFilter = []

            queryParams= [
                    {"name": "page", "value": execution_query_model.page_number},
                    {"name": "limit", "value": execution_query_model.limit},
                    {"name": "agentExecStartDTFrom", "value": execution_query_model.date_from},
                    {"name": "agentExecStartDTTo", "value": execution_query_model.date_to},
                    {"name": "includeTags", "value": execution_query_model.includeTags},
                    {"name": "includeData", "value": execution_query_model.includeData},
                    {"name": "includeErrors", "value": execution_query_model.includeErrors},
                    {"name": "includeEvals", "value": execution_query_model.includeEvals},
                    {"name": "agentExecType", "value": "START"}
                ]

            if (execution_query_model.chamber_id_list != None and len(execution_query_model.chamber_id_list) > 0):
                queryParams.append({"name": "chamberId", "value": json.dumps(execution_query_model.chamber_id_list)})

            if (execution_query_model.agent_id_list != None and len(execution_query_model.agent_id_list) > 0):
                queryParams.append({"name": "agentId", "value": json.dumps(execution_query_model.agent_id_list)})

            if (execution_query_model.agent_deploy_id_list != None and len(execution_query_model.agent_deploy_id_list) > 0):
                queryParams.append({"name": "agentDeployId", "value": ",".join(execution_query_model.agent_deploy_id_list)})

            if (execution_query_model.user_id_list != None and len(execution_query_model.user_id_list) > 0):
                queryParams.append({"name": "agentExecCliUserId", "value": json.dumps(execution_query_model.user_id_list)})

            if (execution_query_model.session_id_list != None and len(execution_query_model.session_id_list) > 0):
                queryParams.append({"name": "agentExecCliSessionId", "value": json.dumps(execution_query_model.session_id_list)})

            if (execution_query_model.channel_id_list != None and len(execution_query_model.channel_id_list) > 0):
                queryParams.append({"name": "agentExecCliChannel", "value": json.dumps(execution_query_model.channel_id_list)})

            if (execution_query_model.environment_id != None):
                queryParams.append({"name": "environmentId", "value": execution_query_model.environment_id})

            if (execution_query_model.isTestPlan != None):
                queryParams.append({"name": "agentExecIsTest", "value": execution_query_model.isTestPlan})

            if (execution_query_model.finished != None):
                queryParams.append({"name": "agentExecSuccessfull", "value": execution_query_model.finished})

            if (execution_query_model.eval_id_user != None and len(execution_query_model.eval_id_user.eval_id) > 0):
                queryParams.append({"name": "evalIdUser", "value": ",".join(execution_query_model.eval_id_user.eval_id)})
                if (execution_query_model.eval_id_user.include == False):
                    excludeFilter.append("EVALIDUSER")

            if (execution_query_model.eval_id_internal != None and len(execution_query_model.eval_id_internal.eval_id) > 0):
                queryParams.append({"name": "evalIdInternal", "value": ",".join(execution_query_model.eval_id_internal.eval_id)})
                if (execution_query_model.eval_id_internal.include == False):
                    excludeFilter.append("EVALIDINTERNAL")

            if (execution_query_model.eval_id_auto != None and len(execution_query_model.eval_id_auto.eval_id) > 0):
                queryParams.append({"name": "evalIdAuto", "value": ",".join(execution_query_model.eval_id_auto.eval_id)})
                if (execution_query_model.eval_id_auto.include == False):
                    excludeFilter.append("EVALIDAUTO")

            if (execution_query_model.data_filter_list != None and len(execution_query_model.data_filter_list) > 0):
                dataValue = json.dumps(list(map(lambda x: x.to_json(), execution_query_model.data_filter_list)))
                #to base64
                bytes = dataValue.encode('ascii')
                dataValue64 = base64.b64encode(bytes).decode('ascii')

                queryParams.append({"name": "dataFilter", "value": dataValue64})

            if (len(excludeFilter) > 0):
                queryParams.append({"name": "exclude", "value": ";".join(excludeFilter)})

            self.message = "starting postRequest"
            huemul_response = HuemulConnection(connect_object=self.connect_object).get_request(
                route = "agentExec/v1/",
                queryParams=queryParams
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.from_response_provider(huemul_response_provider = huemul_response)
            if (self.isSuccessful):
                self.data = [] if len(huemul_response.data_raw) == 0 else list(map(lambda x: ExecutionResponseModel(**x) ,huemul_response.data_raw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self