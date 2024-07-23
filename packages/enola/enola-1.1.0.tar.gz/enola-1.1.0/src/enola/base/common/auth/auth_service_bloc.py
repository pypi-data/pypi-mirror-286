from enola.base.common.auth.auth_service_provider import AuthServiceProvider

class AuthServiceBloc():
    #
    # start authSignInService
    # @param authModel authModel
    # @return HuemulResponseBloc[AuthServiceModel]
    #
    def authSignInService(self, authModel, connectObject):
        continueInLoop = True
        attempt = 0
        #result = HuemulResponseBloc()

        connectObject.huemulLogging.logMessageInfo("Ground Control station: " + authModel.urlService)
        connectObject.huemulCommon.setServiceUrl(value = authModel.urlService)

        while (continueInLoop):
            result = AuthServiceProvider(connect_object=connectObject).authSignInService(
                consumer_id = authModel.consumer_id,
                consumer_secret = authModel.consumer_secret,
                org_id = authModel.org_id,
                application_name = authModel.application_name
            )

            attempt +=1
            continueInLoop = result.analyze_errors(attempt)
        

        return result