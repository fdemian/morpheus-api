from tornado import gen
from .FacebookService import FacebookAuthService
from .GoogleService import GoogleAuthService
from api.authentication.AuthExceptions import OAuthFailedException, NoSuchServiceException
from sqlalchemy.orm.exc import MultipleResultsFound
from api.model.sessionHelper import get_session
from api.model.models import User, OAuthAccount
from api.authentication.AuthExceptions import ExistingUserException
from api.Utils import download_avatar, uglify_username


class OAuthService:

    services = {
        "facebook": FacebookAuthService,
        "google": GoogleAuthService
    }

    def __init__(self, oauth_settings):
        self.oauth_settings = oauth_settings

    def get_service_instance(self, service_type):
        auth_service = self.services.get(service_type)

        if auth_service is None:
            raise NoSuchServiceException

        service_key = self.oauth_settings[service_type]["key"]
        service_secret = self.oauth_settings[service_type]["secret"]
        service_instance = auth_service(service_key, service_secret)

        return service_instance

    @gen.coroutine
    def get_user_by_service(self, service_type, auth_code, redirect_uri):

        service_instance = self.get_service_instance(service_type)
        user = yield service_instance.get(auth_code, redirect_uri, "login")

        if user is None:
            raise OAuthFailedException

        return user

    @gen.coroutine
    def register_user(self, service_type, auth_code, redirect_uri):

        service_instance = self.get_service_instance(service_type)
        oauth_user = yield service_instance.get(auth_code, redirect_uri, "register")
        uglified_username = uglify_username(oauth_user["username"])
        user_avatar = yield download_avatar(oauth_user["avatar"], uglified_username)

        user = User()
        user.username = oauth_user["username"]
        user.fullname = oauth_user["fullname"]
        user.email = oauth_user['email']
        user.valid = True  # Identity verified by the oauth provider.
        user.password = None
        user.salt = None
        user.avatar = user_avatar

        oauth_account = OAuthAccount()
        oauth_account.oauth_id = oauth_user["id"]
        oauth_account.provider = service_type

        saved_user = self.save_user(user, oauth_account)
        oauth_user["avatar"] = user_avatar
		
        return oauth_user        

    @staticmethod
    def save_user(user, oauth_account):

        # Save user.
        session_object = get_session()
        session = session_object()

        try:
            user_exists = session.query(User).filter(User.email == user.email).one_or_none()

            if user_exists is not None:
                raise ExistingUserException

            user.accounts.append(oauth_account)
            session.add(user)
            session.commit()

            return user

        except (MultipleResultsFound, ExistingUserException):
            return None
