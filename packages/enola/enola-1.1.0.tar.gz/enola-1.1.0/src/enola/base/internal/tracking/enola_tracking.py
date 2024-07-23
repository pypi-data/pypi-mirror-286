from enola.base.connect import Connect
from enola.base.internal.tracking.enola_tracking_bloc import EnolaTrackingBloc
from enola.enola_types import TrackingModel, TrackingResponseModel


def create_tracking(tracking_model: TrackingModel, connection: Connect, raise_error_if_fail = True):
    if (not connection.can_execute):
        connection.huemul_logging.log_message_error(message = "cant execute: ")
        return TrackingResponseModel(
            enola_id="",
            agent_deploy_id="",
            url_evaluation_def_get="",
            url_evaluation_post="",
            successfull = False,
            message = "can't execute:"
        )

    #connection.huemul_logging.log_message_info(message = "creating Enola Tracking")

    enola_tracking_result = EnolaTrackingBloc().enola_tracking_create(tracking_model=tracking_model,connect_object=connection)
    #if error
    if (not enola_tracking_result.isSuccessful):
        print(enola_tracking_result)
        connection._can_execute = False
        try:
            connection._error_message = enola_tracking_result.message if (len(enola_tracking_result.errors) == 0) else enola_tracking_result.errors[0]["errorTxt"]
        except:
            connection._error_message = enola_tracking_result.message if (len(enola_tracking_result.errors) == 0) else enola_tracking_result.errors[0].errorTxt

        connection.huemul_logging.log_message_error(message = "error in enolaTracking: " + connection._error_message)

        if (raise_error_if_fail):
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            raise NameError(connection._error_message)
        else:
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            return TrackingResponseModel(
                enola_id="",
                agent_deploy_id="",
                url_evaluation_def_get="",
                url_evaluation_post="",
                successfull = False,
                message = "error " + connection._error_message
            )

    #if all ok, continue
    # connectObject._processExecStepId = enolaAgentResult.data[0].processExecStepId

    return TrackingResponseModel(
        enola_id=enola_tracking_result.data.get("enolaId"),
        agent_deploy_id=enola_tracking_result.data.get("agentDeployId"),
        url_evaluation_def_get=enola_tracking_result.data.get("urlEvaluationDefGet"),
        url_evaluation_post=enola_tracking_result.data.get("urlEvaluationPost"),
        successfull = enola_tracking_result.isSuccessful,
        message = enola_tracking_result.message,
        **enola_tracking_result.data
    )