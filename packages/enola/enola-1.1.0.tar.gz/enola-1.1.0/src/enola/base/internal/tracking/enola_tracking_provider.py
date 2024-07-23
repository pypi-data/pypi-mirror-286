import json
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_response_error import HuemulResponseError
from enola.base.common.huemul_response_to_bloc import HuemulResponseToBloc
from enola.enola_types import TrackingModel, TrackingResponseModel

class EnolaTrackingProvider(HuemulResponseToBloc):
    
    #
    # tracking_create
    # @param TrackingModel trackingModel
    # @return AgentExecuteResponseModel[AgentExecuteResponseModel]
    #
    def tracking_create(self, tracking_model: TrackingModel):
        #self = AgentExecuteResponseModel()
        try:
            hf = HuemulFunctions()
            hf.delete_args(tracking_model)
            #dataIn2 = jsonpickle.encode(agentModel)
            data_in = json.dumps(tracking_model.to_json(), default=lambda o: o.__dict__)
            #dataIn =  agentModel.to_json()

            #dataIn = json.dumps(agentModel, default=lambda obj: obj.__dict__)
            self.message = "starting postRequest"
            huemul_response = HuemulConnection(connect_object=self.connect_object).post_request(
                route = "agent/execute/v1/",
                data = data_in,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.from_response_provider(huemul_response_provider = huemul_response)
            if (self.isSuccessful):
                self.data = [] if len(huemul_response.data_raw) == 0 else list(map(lambda x: TrackingResponseModel(**x) ,huemul_response.data_raw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self