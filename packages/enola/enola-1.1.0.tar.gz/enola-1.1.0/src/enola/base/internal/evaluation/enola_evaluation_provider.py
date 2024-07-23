import json
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_response_error import HuemulResponseError
from enola.base.common.huemul_response_to_bloc import HuemulResponseToBloc
from enola.enola_types import EvaluationModel, EvaluationResponseModel

class EnolaEvaluationProvider(HuemulResponseToBloc):
    
    #
    # evaluation_create
    # @param EvaluationModel evaluationModel
    # @return AgentExecuteResponseModel[AgentExecuteResponseModel]
    #
    def evaluation_create(self, evaluation_model: EvaluationModel):
        #self = AgentExecuteResponseModel()
        try:
            hf = HuemulFunctions()
            hf.delete_args(evaluation_model)
            #dataIn2 = jsonpickle.encode(agentModel)
            data_in = json.dumps(evaluation_model.to_json())

            self.message = "starting postRequest"
            huemul_response = HuemulConnection(connect_object=self.connect_object).post_request(
                route = "agent/eval/v1/",
                data = data_in,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.from_response_provider(huemul_response_provider = huemul_response)
            if (self.isSuccessful):
                self.data = EvaluationResponseModel(**huemul_response.data_raw)
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self