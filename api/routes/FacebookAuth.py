import json
from tornado.auth import FacebookGraphMixin
from tornado.web import RequestHandler

class FacebookAuthService(RequestHandler, FacebookGraphMixin):

    async def get(self, code):
        client_id = self.settings['facebook_api_key']
        client_secret = self.settings['facebook_api_secret']

        user = await self.get_authenticated_user(
            redirect_uri='http://localhost:3000',
            client_id=client_id, client_secret=client_secret
        )

        print(user)
        print(":::::::")

        # user = await oauth_client.http_get(
        #   "https://www.googleapis.com/oauth2/v1/userinfo?{}".format(
        #       url_parse.urlencode({'access_token': str(access["access_token"])})))

        # print(user)

        user_stringify = json.dumps(user)
        self.set_status(200, "Ok")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(user_stringify)
