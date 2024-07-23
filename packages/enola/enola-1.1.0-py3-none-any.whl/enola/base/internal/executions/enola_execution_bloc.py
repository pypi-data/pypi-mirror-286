from enola.base.connect import Connect
from enola.base.internal.executions.enola_execution_provider import EnolaExecutionProvider
from enola.enola_types import ExecutionQueryModel

class EnolaExecutionBloc():
    #
    # start enolaExecutionGet
    # @param AgentModel AgentModel
    # @return HuemulResponseBloc[EnolaAgentResponseModel]
    #
    def enola_execution_get(self, execution_query_model: ExecutionQueryModel, connect_object: Connect):
        (continue_in_loop) = True
        attempt = 0
        #result = HuemulResponseToBloc(connectObject=connectObject)

        while ((continue_in_loop)):
            result = EnolaExecutionProvider(connect_object=connect_object).execution_get(
                    execution_query_model=execution_query_model
            )
            attempt +=1
            (continue_in_loop) = result.analyze_errors(attempt)
        
        return result