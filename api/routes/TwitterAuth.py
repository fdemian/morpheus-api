from tornado.auth import TwitterMixin
from tornado.web import RequestHandler

class TwitterLoginHandler(RequestHandler, TwitterMixin):
    async def get(self):
        if self.get_argument("oauth_token", None):

            user = await self.get_authenticated_user()
            # Save the user using e.g. set_secure_cookie()
            print(user)

            self.set_status(200, "Ok")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write("OK!!!!")