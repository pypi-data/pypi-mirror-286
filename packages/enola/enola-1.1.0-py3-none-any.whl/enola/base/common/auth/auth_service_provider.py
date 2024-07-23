import base64
from enola.base.common.auth.auth_service_model import AuthServiceModel
from enola.base.common.huemul_connection import HuemulConnection
from enola.base.common.huemul_response_error import HuemulResponseError
from enola.base.common.huemul_response_to_bloc import HuemulResponseToBloc

class AuthServiceProvider(HuemulResponseToBloc):
    
    #
    # create new element
    # @param consumer_id consumer_id: String
    # @param consumerSecret consumerSecret: String
    # @param org_id orgIorg_idd: String
    # @param applicationName applicationName: String
    #
    def authSignInService(self, consumer_id, consumer_secret, org_id, application_name):
        try:
            dataIn = consumer_id + ":" + consumer_secret
            bytes = dataIn.encode('ascii') #.getBytes(StandardCharsets.UTF_8)
            base64Str = base64.b64encode(bytes).decode('ascii')

            huemulResponse = HuemulConnection(connect_object=self.connect_object).auth_request(
                route = "authService/v1/sign-in-service/",
                data = base64Str,
                org_id = org_id
            )

            #get status from connection
            self.from_response_provider(huemul_response_provider = huemulResponse)
            if (self.isSuccessful):
                self.data = [] if len(huemulResponse.data_raw) == 0 else list(map(lambda x: AuthServiceModel(**x) ,huemulResponse.data_raw))
        except Exception as e:
            self.errors.append(
                HuemulResponseError(errorId = "APP-101", errorTxt = str(e))
            )

        return self


        