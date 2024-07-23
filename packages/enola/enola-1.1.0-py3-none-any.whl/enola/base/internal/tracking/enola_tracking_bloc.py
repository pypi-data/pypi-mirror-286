from enola.base.connect import Connect
from enola.base.internal.tracking.enola_tracking_provider import EnolaTrackingProvider
from enola.enola_types import TrackingModel


class EnolaTrackingBloc():
    #
    # start enolaAgentCreate
    # @param AgentModel AgentModel
    # @return HuemulResponseBloc[EnolaAgentResponseModel]
    #
    def enola_tracking_create(self, tracking_model: TrackingModel, connect_object: Connect):
        (continue_in_loop) = True
        attempt = 0
        #result = HuemulResponseToBloc(connectObject=connectObject)

        while ((continue_in_loop)):
            result = EnolaTrackingProvider(connect_object=connect_object).tracking_create(
                    tracking_model=tracking_model
            )
            attempt +=1
            (continue_in_loop) = result.analyze_errors(attempt)
        
        return result