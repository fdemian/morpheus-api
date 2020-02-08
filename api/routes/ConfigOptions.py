from tornado.web import RequestHandler
from tornado.gen import coroutine


class ConfigHandler(RequestHandler):

    def get(self):

        """
        Return application configuration parameters.
        This route only returns parameters that are public.
        All API secrets and other parameters are not returned.
        """

        try:

            response = {
                "oauth": [
                    {
                            'name': 'facebook',
                            'key': self.settings["facebook_api_key"],
                            'authorizeURL': self.settings["facebook_redirect_url"],
                    },
                    {
                            'name': 'google',
                            'key': self.settings["google_oauth_key"],
                            'authorizeURL': self.settings["google_redirect_url"],
                    }],
                "notificationsEnabled": self.settings['notifications_enabled'],
                "blogName": self.settings['blog_name']
            }

            self.set_status(200, 'Ok')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

        except:

            response = {'message': "Could not read configuration options."}

            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

        return

    @coroutine
    def put(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def delete(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def trace(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def connect(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def options(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def patch(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def head(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return
