from api.Utils import validate_token
from tornado.web import RequestHandler


class AuthenticatedHandler(RequestHandler):

    def get_current_user(self):
        #auth_headers = self.request.headers.get("Authorization")
        auth_headers = self.request.headers.get("Cookie")

        if auth_headers is None:
            return None
        
        jwt_token = auth_headers.split("=")[1]
        jwt_secret = self.settings["jwt_secret"]
        jwt_algorhitm = self.settings["jwt_algorithm"]
        validated_user = validate_token(jwt_token, jwt_secret, jwt_algorhitm)

        if validated_user is None:
            return None

        # Perform additional validation on JWT claims.
        decoded_id = int(self.get_secure_cookie("user", value=validated_user["user_token"]))

        if decoded_id is None:
            return None

        return decoded_id
