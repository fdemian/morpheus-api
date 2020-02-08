import tornado
import tornado.web
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import RequestHandler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.model.sessionHelper import get_session
from api.model.models import User


class GoogleAuthService(GoogleOAuth2Mixin):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    async def get(self, auth_code, redirect_url, method):

        await print("::::::::::::::::::::::::::::")
        google_user = await self.get_authenticated_user(redirect_uri=redirect_url, code=auth_code)
        await print(google_user)
        await print("..................")
        await print("PETE WALLANDER")

        if not google_user:
            yield None

        if method == "login":
            user = self.get_user_from_db(google_user)
        elif method == "register":
            user = self.get_user_to_save(google_user)

        yield user

    @staticmethod
    def get_user_to_save(google_user):

        payload = {
            'id': google_user["sub"],
            'avatar': google_user["picture"],
            'username': google_user["name"],
            'fullname': google_user["name"],
            'email': google_user['email'],
            'role': 'author'
        }

        return payload

    @staticmethod
    def get_user_from_db(google_user):

        try:
            session_object = get_session()
            session = session_object()
            user = session.query(User).filter(User.email == google_user['email']).one()

            user_link = '/users/' + str(user.id) + "/" + user.username

            payload = {
                'id': user.id,
                'avatar': user.avatar,
                'username': user.username,
                'role': 'author',
                'link': user_link
            }

        except MultipleResultsFound:
            payload = None

        except NoResultFound:

            payload = {
                'id': google_user["sub"],
                'avatar': google_user["picture"],
                'username': google_user["name"],
                'role': 'guest',
                'link': google_user["profile"]
            }

        return payload

