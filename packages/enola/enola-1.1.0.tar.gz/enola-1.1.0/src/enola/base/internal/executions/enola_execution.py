from enola.base.connect import Connect
from enola.base.internal.executions.enola_execution_bloc import EnolaExecutionBloc
from enola.enola_types import ExecutionModel, ExecutionQueryModel


def get_execution(execution_query_model: ExecutionQueryModel, connection: Connect, raise_error_if_fail = True) -> ExecutionModel:
    if (not connection.can_execute):
        connection.huemul_logging.log_message_error(message = "can't execute: ")
        return ExecutionModel(
                data=[],
                successfull=False,
                message="Not Executed yet, can't execute:"
            )

    connection.huemul_logging.log_message_info(message = "Running Enola Execution")

    enola_execution_result = EnolaExecutionBloc().enola_execution_get(execution_query_model=execution_query_model,connect_object=connection)
    #if error
    if (not enola_execution_result.isSuccessful):
        print(enola_execution_result)
        connection._can_execute = False
        try:
            connection._error_message = enola_execution_result.message if (len(enola_execution_result.errors) == 0) else enola_execution_result.errors[0]["errorTxt"]
        except:
            connection._error_message = enola_execution_result.message if (len(enola_execution_result.errors) == 0) else enola_execution_result.errors[0].errorTxt

        connection.huemul_logging.log_message_error(message = "error in enolaExecution: " + connection._error_message)

        if (raise_error_if_fail):
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            raise NameError(connection._error_message)
        else:
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            return ExecutionModel(
                data=[],
                successfull=False,
                message="error " + connection._error_message,
            )

    #if all ok, continue
    # connectObject._processExecStepId = enolaAgentResult.data[0].processExecStepId

    return ExecutionModel(
        data=enola_execution_result.data,
        successfull=enola_execution_result.isSuccessful,
        message=enola_execution_result.message,
    )