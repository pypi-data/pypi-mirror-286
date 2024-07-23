import requests
from enola.base.common.huemul_http_info import HuemulHttpInfo
from enola.base.common.huemul_response_provider import HuemulResponseProvider
from enola.base.common.huemul_response_error import HuemulResponseError
import json

from enola.base.connect import Connect

class HuemulConnection:
    def __init__(self, connect_object: Connect):
        self.connectObject = connect_object
        #self.httpClient: CloseableHttpClient = HttpClients.createDefault

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    #
    # get HTTP call to post method
    # @param route url
    # @param data info to be sent to post method
    # @return
    #
    def auth_request(self, route, data, org_id):
        if (self.connectObject.huemul_common.get_service_url() == ""):
            raise NameError('API Url null or empty')

        httpInfo = HuemulHttpInfo("", -1)

        try:
            # create object
            uriFinal = self.connectObject.huemul_common.get_service_url() + route

            #add header
            headers = self.get_header_for_auth({
                "authorization" : "Basic " + data,
                "orgId": org_id,
            })

            payload = "".format("")
            httpInfo = requests.request("POST", uriFinal, data=payload, headers=headers)
            # print(response.text)
        except Exception as e:
            print(e)
            

        value = self._get_response(httpInfo)
        return value
        

    #
    # get HTTP call to get method
    # @param route url
    # @param queryParams query params
    # @param headerParams header params
    # @return
    #
    def get_request(self, route, queryParams = [], headerParams = None):
        huemul_response_on_error = HuemulResponseProvider() #used only if error exists

        if (self.connectObject.huemul_common.get_service_url() == ""):
            raise NameError('API Url null or empty')

        routeParams = ""
        for i in range(len(queryParams)):
            routeParams = routeParams + ("?" if i == 0 else "&") + str(queryParams[i].get("name")) + "=" + str(queryParams[i].get("value"))
        
        httpInfo = HuemulHttpInfo("", -1)

        try:
            # create object
            uriFinal = self.connectObject.huemul_common.get_service_url() + route + routeParams

            #add header
            headers = self.get_header(headerParams=headerParams)

            httpInfo = requests.request("GET", uriFinal, headers=headers)
            # print(response.text)

            value = self._get_response(httpInfo)
            return value
        except requests.exceptions.HTTPError as http_err:
            error_code = httpInfo.status_code if 'httpInfo' in locals() else None
            print(f'HTTP error occurred: {http_err}')  # Nombre del error y descripción
            print(f'HTTP status code: {error_code}')
            
            huemul_response_on_error.errors.append(HuemulResponseError(errorId = error_code, errorTxt = str(http_err)))
        except requests.exceptions.ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')  # Nombre del error y descripción
            huemul_response_on_error.errors.append(HuemulResponseError(errorId = "ConnectionError", errorTxt = str(conn_err)))
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')  # Nombre del error y descripción
            huemul_response_on_error.errors.append(HuemulResponseError(errorId = "Timeout", errorTxt = str(timeout_err)))
        except requests.exceptions.RequestException as req_err:
            print(f'An error occurred: {req_err}')  # Nombre del error y descripción
            huemul_response_on_error.errors.append(HuemulResponseError(errorId = "RequestException", errorTxt = str(req_err)))
        except Exception as e:
            print(e)
            huemul_response_on_error.errors.append(HuemulResponseError(errorId = "connection_other", errorTxt = str(e)))

        return huemul_response_on_error
        

    #
    # get HTTP call to post method
    # @param route url
    # @param queryParams query params
    # @param data info to be sent to post method
    # @return
    #
    def post_request(self, route, data, queryParams = [], headerParams = None):
        if (self.connectObject.huemul_common.get_service_url() == ""):
            raise NameError('API Url null or empty')

        routeParams = ""
        for i in range(len(queryParams)):
            routeParams = routeParams + ("?" if i == 0 else "&") + str(queryParams[0].name) + "=" + str(queryParams[0].value)
        
        httpInfo = HuemulHttpInfo("", -1)

        try:
            # create object
            uriFinal = self.connectObject.huemul_common.get_service_url() + route + routeParams

            #add header
            headers = self.get_header(headerParams=headerParams)

            payload = data #"".format("")
            httpInfo = requests.request("POST", uriFinal, data=payload, headers=headers)
            # print(response.text)

            value = self._get_response(httpInfo)
            return value
        except Exception as e:
            print(e)
            huemulResponse = HuemulResponseProvider()
            huemulResponse.errors.append(HuemulResponseError(errorId = "post_error", errorTxt = str(e)))

            return huemulResponse

            
        

    #
    # get HTTP call to post method
    # @param route url
    # @param queryParams query params
    # @param data info to be sent to put method
    # @return
    #
    def put_request(self, route, data, queryParams = []):
        if (self.connectObject.huemul_common.get_service_url() == ""):
            raise NameError('API Url null or empty')

        routeParams = ""
        for i in range(len(queryParams)):
            routeParams = routeParams + ("?" if i == 0 else "&") + str(queryParams[0].name) + "=" + str(queryParams[0].value)
        
        httpInfo = HuemulHttpInfo("", -1)

        try:
            # create object
            uriFinal = self.connectObject.huemul_common.get_service_url() + route + routeParams

            #add header
            headers = self.get_header(headerParams=None)

            payload = data #"".format("")
            httpInfo = requests.request("PUT", uriFinal, data=payload, headers=headers)
            # print(response.text)
        except Exception as e:
            print(e)
            
        value = self._get_response(httpInfo)
        return value

    #
    # common header for each http method
    # headerParams: Dictionary
    # @return Dictionary
    #
    def get_header_for_auth(self, headerParams):
        dataToReturn = {
            "Accept" : "application/json",
            "content-type" : "application/json",
            "huemul-client-language" : "PYTHON",
            "huemul-client-version" : "1.0",
            "huemul-client-app" : "SERVER",
            "huemul-client-info" : "",
        }

        if (headerParams != None):
            dataToReturn.update(headerParams)

        return dataToReturn


    #
    # common header for each http method
    # headerParams: Dictionary
    # @return Dictionary
    #
    def get_header(self, headerParams):
        dataToReturn = {
            "Accept" : "application/json",
            "content-type" : "application/json",
            "huemul-client-language" : "PYTHON",
            "huemul-client-version" : "1.0",
            "huemul-client-app" : "SERVER",
            "huemul-client-info" : "",
            "authorization": "Bearer " + self.connectObject.huemul_common.get_token_id(),
            "orgId" : self.connectObject.huemul_common.get_org_id()
        }

        if (headerParams != None): 
            dataToReturn.update(headerParams)

        return dataToReturn


    # transform data from api to response
    # response: HuemulHttpInfo
    # return HuemulResponseProvider
    def _get_response(self, response):
        huemulResponse = HuemulResponseProvider()

        try:
            if (response.text != ""):
                dataFromJson = json.loads(response.text)
                huemulResponse.fromDict(**dataFromJson)
            else:
                huemulResponse.isSuccessful = False
                huemulResponse.errors.append(HuemulResponseError(errorId = "getResponseError", errorTxt = f'status {response.status_code}: response.text is empty'))
                huemulResponse.httpStatusCode = response.status_code
                huemulResponse.message = response.reason
            
            #huemulResponse.fromDict(**dataFromJson) #HuemulResponseProvider.fromJson(response.text)
        except Exception as e:
            #huemulResponse.isSuccessful = false;
            huemulResponse.errors.append(HuemulResponseError(errorId = "getResponseError", errorTxt = str(e)))
        
        return huemulResponse