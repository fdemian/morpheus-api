import tornado
import tornado.web
import tornado.auth
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.model.sessionHelper import get_session
from api.model.models import User


class TwitterService(tornado.web.RequestHandler, tornado.auth.TwitterMixin):

    @tornado.gen.coroutine
    def get(self, auth_code, redirect_url):

        #user = self.get_user(fb_user)

        return None

    @staticmethod
    def get_user(fb_user):

        try:
            session_object = get_session()
            session = session_object()
            user = session.query(User).filter(User.email == fb_user['email']).one()

            payload = {
                'id': user.id,
                'avatar': user.avatar,
                'username': user.username,
                'role': 'author',
                'link': fb_user["link"]
            }

        except MultipleResultsFound:
            payload = None

        except NoResultFound:

            if not fb_user['picture']['data']['is_silhouette']:
                picture = fb_user['picture']['data']['url']
            else:
                picture = ""

            payload = {
                'id': fb_user["id_str"],
                'avatar': picture,
                'username': fb_user["name"],
                'role': 'guest',
                'link': fb_user["link"]
            }

        return payload

