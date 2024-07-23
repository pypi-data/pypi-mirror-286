from enola.base.connect import Connect
from enola.base.internal.tracking_batch.enola_tracking_batch_provider import EnolaTrackingBatchProvider
from enola.enola_types import TrackingModel, TrackingBatchHeadModel
from typing import List

class EnolaTrackingBatchBloc():
    #
    # start enolaAgentCreate
    # @param AgentModel AgentModel
    # @return HuemulResponseBloc[EnolaAgentResponseModel]
    #
    def enola_tracking_batch_create(self, tracking_list_model: List[TrackingModel], connect_object: Connect):
        """
        Start tracking Batch Execution
        """
        (continue_in_loop) = True
        attempt = 0
        #result = HuemulResponseToBloc(connectObject=connectObject)

        while ((continue_in_loop)):
            result = EnolaTrackingBatchProvider(connect_object=connect_object).tracking_batch_create(
                    tracking_list_model=tracking_list_model
            )
            attempt +=1
            (continue_in_loop) = result.analyze_errors(attempt)
        
        return result
    

    def enola_tracking_batch_head_create(self, tracking_batch_head_model: TrackingBatchHeadModel, connect_object: Connect):
        """
        Start tracking Batch Head Execution
        """
        (continue_in_loop) = True
        attempt = 0
        #result = HuemulResponseToBloc(connectObject=connectObject)

        while ((continue_in_loop)):
            result = EnolaTrackingBatchProvider(connect_object=connect_object).tracking_batch_head_create(
                    tracking_batch_head_model=tracking_batch_head_model
            )
            attempt +=1
            (continue_in_loop) = result.analyze_errors(attempt)
        
        return result