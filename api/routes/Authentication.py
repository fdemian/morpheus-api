import jwt
import json
from datetime import datetime, timedelta
from api.authentication.Database import DatabaseAuthService
from api.authentication.AuthExceptions import OAuthFailedException, NoSuchServiceException, InvalidUserException
from api.Utils import get_oauth_settings
from tornado.web import RequestHandler
from tornado.gen import coroutine

class Authentication(RequestHandler):

    def data_received(self, chunk):
        pass

    async def post(self):

        try:
            request = self.request.body.decode('utf-8')
            json_request = json.loads(json.loads(request))

            auth_code = json_request['code']
            auth_type = json_request['type']
            redirect_url = json_request["redirectURL"]

            username = json_request['username']
            password = json_request['password']

            authentication = DatabaseAuthService()
            user = authentication.authenticate_user(username, password, self.settings)

            if user is not None:

              jwt_token = self.perform_authentication(user, auth_type, '3600')
              str_token = str(jwt_token.decode('utf-8'))
              user_id = str(user['id'])
              token_header = "access_token=" + str_token

              response = {'id': user_id }

              self.set_status(200, 'Ok')
              self.set_header("Access-Control-Allow-Origin", "*")
              self.set_header("Set-Cookie", token_header)

              self.write(response)
              return

            else:
              response = {'message': "The user/password combination is invalid."}
              self.set_status(401, 'Error')
              self.set_header("Access-Control-Allow-Origin", "*")
              self.write(response)
              return

        except OAuthFailedException:
            response = {'message': "An error occurred authenticating the user."}
            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)
            return

        except NoSuchServiceException:
            response = {'message': "The specified oauth service does not exist or is not enabled."}
            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)
            return

        except:
            response = {'message': "Internal server error."}
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

    # Helper method (move?)
    def perform_authentication(self, user, auth_type, expires):

        user_id = str(user["id"])
        user_token = self.create_signed_value("user", user_id).decode('utf-8')
        jwt_expiration = self.settings["jwt_expiration_seconds"]
        expdate = datetime.utcnow() + timedelta(int(jwt_expiration))

        jwt_payload = {
            'user_token': user_token,
            'type': auth_type,
            'exp': expdate
        }

        jwt_token = jwt.encode(jwt_payload, self.settings["jwt_secret"], algorithm=self.settings["jwt_algorithm"])

        return jwt_token
