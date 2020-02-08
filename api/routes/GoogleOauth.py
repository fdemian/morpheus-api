import json
import sys
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import RequestHandler
#from tornado import gen
#from api.Utils import get_oauth_settings

TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'

class GoogleAuthService(RequestHandler, GoogleOAuth2Mixin):

    async def get(self, code):
        user = await self.get_authenticated_user(redirect_uri='http://localhost:3000',code=code)

        print(user)

        user_stringify = json.dumps(user)
        self.set_status(200, "Ok")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(user_stringify)