from enola.base.connect import Connect
from enola.base.internal.evaluation.enola_evaluation_bloc import EnolaEvaluationBloc
from enola.enola_types import EvaluationModel, EvaluationResponseModel


def create_evaluation(evaluation_model: EvaluationModel, connection: Connect, raise_error_if_fail = True):
    if (not connection.can_execute):
        connection.huemul_logging.log_message_error(message = "can't execute: ")
        return EvaluationResponseModel(
            enola_id = "",
            agent_deploy_id = "",
            enola_eval_id = "",
            successfull = False,
            message = "can't execute:"
        )

    connection.huemul_logging.log_message_info(message = "creating Enola Evaluation")

    enola_evaluation_result = EnolaEvaluationBloc().enola_evaluation_create(evaluation_model=evaluation_model,connect_object=connection)
    #if error
    if (not enola_evaluation_result.isSuccessful):
        print(enola_evaluation_result)
        connection._can_execute = False
        try:
            connection._error_message = enola_evaluation_result.message if (len(enola_evaluation_result.errors) == 0) else enola_evaluation_result.errors[0]["errorTxt"]
        except:
            connection._error_message = enola_evaluation_result.message if (len(enola_evaluation_result.errors) == 0) else enola_evaluation_result.errors[0].errorTxt

        connection.huemul_logging.log_message_error(message = "error in enolaEvaluation: " + connection._error_message)

        if (raise_error_if_fail):
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            raise NameError(connection._error_message)
        else:
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            return EvaluationResponseModel(
                enola_id = "",
                agent_deploy_id = "",
                enola_eval_id = "",
                successfull = False,
                message = "error " + connection._error_message
            )

    #if all ok, continue
    # connectObject._processExecStepId = enolaAgentResult.data[0].processExecStepId

    return EvaluationResponseModel(
        successfull = enola_evaluation_result.isSuccessful,
        message = enola_evaluation_result.message,
        enola_eval_id= enola_evaluation_result.data.enola_eval_id,
        enola_id = enola_evaluation_result.data.enola_id,
        agent_deploy_id = enola_evaluation_result.data.agent_deploy_id
    )