from enola.base.connect import Connect
from enola.base.internal.tracking_batch.enola_tracking_batch_bloc import EnolaTrackingBatchBloc
from enola.enola_types import TrackingBatchDetailResponseModel, TrackingBatchHeadModel, TrackingBatchHeadResponseModel, TrackingModel, TrackingResponseModel
from typing import List


def create_tracking_batch_head(tracking_batch_model: TrackingBatchHeadModel, connection: Connect, raise_error_if_fail = True):
    if (not connection.can_execute):
        connection.huemul_logging.log_message_error(message = "cant execute: ")
        return TrackingBatchHeadResponseModel(
            batch_id="",
            agent_deploy_id="",
            successfull = False,
            message = "can't execute:"
        )

    #connection.huemul_logging.log_message_info(message = "creating Enola Tracking Batch Head")
    enola_tracking_head_result = EnolaTrackingBatchBloc().enola_tracking_batch_head_create(
        tracking_batch_head_model=tracking_batch_model, 
        connect_object=connection
        )
    
    if (not enola_tracking_head_result.isSuccessful):
        print(enola_tracking_head_result)
        connection._can_execute = False
        try:
            connection._error_message = enola_tracking_head_result.message if (len(enola_tracking_head_result.errors) == 0) else enola_tracking_head_result.errors[0]["errorTxt"]
        except:
            connection._error_message = enola_tracking_head_result.message if (len(enola_tracking_head_result.errors) == 0) else enola_tracking_head_result.errors[0].errorTxt

        connection.huemul_logging.log_message_error(message = "error in enolaTrackingBatchHead: " + connection._error_message)

        if (raise_error_if_fail):
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            raise NameError(connection._error_message)
        else:
            connection.huemul_logging.log_message_error(message = "error " + connection._error_message)
            return TrackingBatchHeadResponseModel(
                batch_id="",
                agent_deploy_id="",
                successfull = False,
                message = "error " + connection._error_message
            )

    #if all ok, continue
    # connectObject._processExecStepId = enolaAgentResult.data[0].processExecStepId
    if (len(enola_tracking_head_result.data) == 0):
        return TrackingBatchHeadResponseModel(
                batch_id="",
                agent_deploy_id="",
                successfull = False,
                message = "error, not data found in creating batch head"
            )

    return TrackingBatchHeadResponseModel(
        batch_id=enola_tracking_head_result.data[0].get("agentExecBatchId"),
        agent_deploy_id=enola_tracking_head_result.data[0].get("agentDeployId"),
        successfull = enola_tracking_head_result.isSuccessful,
        message = enola_tracking_head_result.message,
        **enola_tracking_head_result.data[0]
    )


def create_tracking(tracking_list_model: List[TrackingModel], connection: Connect, raise_error_if_fail = True) -> TrackingBatchDetailResponseModel:
    if (not connection.can_execute):
        connection.huemul_logging.log_message_error(message = "cant execute: ")
        return TrackingBatchDetailResponseModel(
            tracking_list=tracking_list_model,
            agent_deploy_id="",
            successfull = False,
            message = "can't execute:"
        )

    #connection.huemul_logging.log_message_info(message = "creating Enola Tracking")
    enola_tracking_result = EnolaTrackingBatchBloc().enola_tracking_batch_create(tracking_list_model=tracking_list_model,connect_object=connection)
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
            return TrackingBatchDetailResponseModel(
                tracking_list=[],
                agent_deploy_id="",
                successfull = False,
                message = "error " + connection._error_message
            )

    #if all ok, continue
    return enola_tracking_result.data[0]