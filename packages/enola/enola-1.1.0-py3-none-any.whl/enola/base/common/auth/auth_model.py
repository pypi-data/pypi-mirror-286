
# consumer_id: String,
# consumer_secret: String,
# org_id: String,
# application_name: String,
# url_service: String
class AuthModel:
    def __init__(self, consumer_id:str = "", consumer_secret:str = "", org_id:str = "", application_name:str = "", url_service:str = "", session_id:str = "", jwt_token: str = ""):
        self.consumer_id = consumer_id
        self.consumer_secret = consumer_secret
        self.org_id = org_id
        self.application_name = application_name
        self.url_service = url_service
        self.sessionId = session_id
        self.jwt_token = jwt_token
        