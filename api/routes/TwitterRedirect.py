from tornado import gen
from tornado.web import RequestHandler
from tornado.auth import TwitterMixin, AuthError
from tornado.escape import json_encode
from api.model.sessionHelper import get_session
from api.model.models import User
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound


class TwitterHandler(RequestHandler, TwitterMixin):

    @gen.coroutine
    def get(self):

        if self.get_argument("oauth_token", None):
            response = yield self.get_authenticated_user(include_email="true")

            # Save the user using e.g. set_secure_cookie()
            del response["description"]
            twitter_user = json_encode(response)

            if not twitter_user:
                return None

            user = self.get_user(twitter_user)

            return user

        else:
            yield self.authorize_redirect()

    @staticmethod
    def get_user(twitter_user):

        try:
            session_object = get_session()
            session = session_object()
            user = session.query(User).filter(User.email == twitter_user['email']).one()

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
                'id': twitter_user["id_str"],
                'avatar': twitter_user["profile_image_url"],
                'username': twitter_user["name"],
                'role': 'guest',
                'link': ""  # Twitter does not provide a link to its users profile by default.
            }

        return payload