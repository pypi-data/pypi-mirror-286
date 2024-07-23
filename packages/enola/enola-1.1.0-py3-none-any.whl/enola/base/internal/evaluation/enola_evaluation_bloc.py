from enola.base.connect import Connect
from enola.base.internal.evaluation.enola_evaluation_provider import EnolaEvaluationProvider
from enola.enola_types import EvaluationModel

class EnolaEvaluationBloc():
    #
    # start enolaAgentCreate
    # @param AgentModel AgentModel
    # @return HuemulResponseBloc[EnolaAgentResponseModel]
    #
    def enola_evaluation_create(self, evaluation_model: EvaluationModel, connect_object: Connect):
        (continue_in_loop) = True
        attempt = 0
        #result = HuemulResponseToBloc(connectObject=connectObject)

        while ((continue_in_loop)):
            result = EnolaEvaluationProvider(connect_object=connect_object).evaluation_create(
                    evaluation_model=evaluation_model
            )
            attempt +=1
            (continue_in_loop) = result.analyze_errors(attempt)
        
        return result