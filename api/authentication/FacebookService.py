from tornado.auth import FacebookGraphMixin
from tornado.gen import coroutine
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.model.sessionHelper import get_session
from api.model.models import User


class FacebookAuthService(FacebookGraphMixin):

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    @coroutine
    def get(self, auth_code, redirect_url, method):

        print(".................")
        print(self.get_authenticated_user)
        print(".................")

        user_info = yield self.get_authenticated_user(
              redirect_uri=redirect_url,
              client_id=self.key,
              client_secret=self.secret,
              code=auth_code)

        print(user_info)

        if not 'email' in user_info:
            # expires_in = user_info["session_expires"][0]
            access_token = user_info["access_token"]        
            user_fields = "id,name,email,picture,link"
            params = {'scope': 'email'}
            fb_user = yield self.facebook_request("/me", access_token=access_token, extra_params=params, fields=user_fields)

            if not fb_user:
                return None
        else:
            fb_user = user_info

        if method == "login":
            user = self.get_user_from_db(fb_user)
        elif method == "register":
            user = self.get_user_to_save(fb_user)

        return user

    @staticmethod
    def get_user_to_save(fb_user):

        if not fb_user['picture']['data']['is_silhouette']:
            picture = fb_user['picture']['data']['url']
        else:
            picture = ""

        payload = {
            'id': fb_user["id"],
            'avatar': picture,
            'username': fb_user["name"],
            'fullname': fb_user["name"],
            'email': fb_user["email"],
            'role': 'author'
        }

        return payload

    @staticmethod
    def get_user_from_db(fb_user):

        try:
            session_object = get_session()
            session = session_object()
            user = session.query(User).filter(User.email == fb_user['email']).one()

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

            if not fb_user['picture']['data']['is_silhouette']:
                picture = fb_user['picture']['data']['url']
            else:
                picture = ""

            payload = {
                'id': fb_user["id"],
                'avatar': picture,
                'username': fb_user["name"],
                'role': 'guest',
                'link': fb_user["link"]
            }

        return payload
