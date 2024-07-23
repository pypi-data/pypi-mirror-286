import json
from enola.base.common.huemul_functions import HuemulFunctions
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_response_error import HuemulResponseError
from enola.base.common.huemul_response_to_bloc import HuemulResponseToBloc
from enola.enola_types import TrackingBatchDetailResponseModel, TrackingBatchHeadModel, TrackingBatchHeadResponseModel, TrackingModel, TrackingResponseModel
from typing import List

class EnolaTrackingBatchProvider(HuemulResponseToBloc):
    
    #
    # tracking_create
    # @param TrackingModel trackingModel
    # @return AgentExecuteResponseModel[AgentExecuteResponseModel]
    #
    def tracking_batch_create(self, tracking_list_model: List[TrackingModel]):
        #self = AgentExecuteResponseModel()
        try:
            hf = HuemulFunctions()
            hf.delete_args(tracking_list_model)
            
            #data_in = json.dumps(tracking_model.to_json(), default=lambda o: o.__dict__)
            data_in =  json.dumps([model.to_json() for model in tracking_list_model])

            #dataIn = json.dumps(agentModel, default=lambda obj: obj.__dict__)
            self.message = "starting postRequest"
            huemul_response = HuemulConnection(connect_object=self.connect_object).post_request(
                route = "agent_batch_detail/execute/v1/",
                data = data_in,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.from_response_provider(huemul_response_provider = huemul_response)
            if (self.isSuccessful):
                self.data = [] if len(huemul_response.data_raw) == 0 else list(map(lambda x: TrackingBatchDetailResponseModel(**x) ,huemul_response.data_raw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self
    
    def tracking_batch_head_create(self, tracking_batch_head_model: TrackingBatchHeadModel):
        #self = AgentExecuteResponseModel()
        try:
            hf = HuemulFunctions()
            hf.delete_args(tracking_batch_head_model)
            data_in = json.dumps(tracking_batch_head_model.to_json(), default=lambda o: o.__dict__)

            self.message = "starting postRequest"
            huemul_response = HuemulConnection(connect_object=self.connect_object).post_request(
                route = "agent_batch_head/execute/v1/",
                data = data_in,
            )

            #get status from connection
            self.message = "starting fromResponseProvider"
            self.from_response_provider(huemul_response_provider = huemul_response)
            if (self.isSuccessful):
                self.data = [] if len(huemul_response.data_raw) == 0 else list(map(lambda x: TrackingBatchHeadResponseModel(**x) ,huemul_response.data_raw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self