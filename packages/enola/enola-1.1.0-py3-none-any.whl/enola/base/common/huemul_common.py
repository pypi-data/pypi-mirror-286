
class HuemulCommon:

    def __init__(self):
        self._service_url = ""

    def __getitem__(self, key):
        return self.__dict__[key]

    def __getattr__(self, key):
        return self.__dict__[key]

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    #
    # return total attemps
    # @return int
    def get_total_attempt(self):
        return 5

    #**********************************************************************
    #***********  S E R V I C E   U R L    ********************************
    #**********************************************************************

    _service_url = ""

    #
    # get Service Url
    # @return ServiceUrl: string
    def get_service_url(self):
        if (self._service_url != "" and self._service_url[-1] != "/"):
            self._service_url = self._service_url + "/"

        return self._service_url


    # set serviceUrl
    # value: string
    def set_service_url(self, value):
        self._service_url = value


    #**********************************************************************
    #***********  T O K E N   I D    **************************************
    #**********************************************************************

    #return string
    _token_id = ""

    #
    # get user Token Id
    # @return TokenId
    #
    def get_token_id(self):
        return self._token_id

    #
    # set tokenID
    # value: string
    #
    def set_token_id(self, value):
        self._token_id = value


    #**********************************************************************
    #***********  O R G   I D    **************************************
    #**********************************************************************

    _org_id = ""

    #
    # get user org Id
    # @return org_id
    #
    def get_org_id(self):
        return self._org_id

    #set org_id
    #value: string
    def set_org_id(self, value):
        self._org_id = value


    #**********************************************************************
    #***********  C O N S U M E R   I D    ********************************
    #**********************************************************************

    _consumer_id = ""

    #
    # get user Consumer Id
    # @return consumer_id
    #
    def get_consumer_id(self):
        return self._consumer_id

    #set consumer_id
    def set_consumer_id(self, value):
        self._consumer_id = value

    #**********************************************************************
    #***********  J W T    T O K E N    ********************************
    #**********************************************************************

    _jwt_token = ""

    #
    # get user Consumer Id
    # @return jwtToken
    #
    def get_jwt_token(self):
        return self._jwt_token

    #set jwtToken
    def set_jwt_token(self, value):
        self._jwt_token = value

    #**********************************************************************
    #***********  C O N S U M E R   S E C R E T    ************************
    #**********************************************************************

    _consumer_secret = ""

    #
    # get user Consumer Secret
    # @return ConsumerSecret
    #
    def get_consumer_secret(self):
        return self._consumer_secret

    #set consumerSecret
    def set_consumer_secret(self, value):
        self._consumer_secret = value

    #**********************************************************************
    #***********  A P P L I C A T I O N   I D    ********************************
    #**********************************************************************

    _application_name = ""

    #
    # get user Application Id
    # @return _applicationName
    #
    def get_application_name(self):
        return self._application_name

    #set applicationName
    def set_application_name(self, value):
        self._application_name = value