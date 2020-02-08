import tornado
import tornado.web
from .GithubMixin import GithubOAuth2Mixin
from tornado.web import RequestHandler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.model.sessionHelper import get_session
from api.model.models import User
from tornado.httpclient import AsyncHTTPClient
from urllib.parse import urlencode

def on_user_obtained(user):
    print(user)

"""
class GithubAuthService(RequestHandler, GithubOAuth2Mixin):

    @tornado.gen.coroutine
    def get(self, auth_code, redirect_url):


        options = get_oauth_settings()

        github_token_request_url = "https://github.com/login/oauth/access_token"
        github_user_info_endpoint = "https://api.github.com/user"

        args = {
                    "client_id": options.github_client_id,
                    "client_secret": options.github_client_secret,
                    "redirect_uri": redirect_url,
                    "code": auth_code
        }

        user = yield self.get_authenticated_user(
            redirect_uri=redirect_url,
            client_id=options.github_client_id,
            client_secret=options.github_client_secret,
            code=auth_code,
            callback=on_user_obtained
        )

        # access = yield self.oauth2_request(github_token_request_url, post_args=args)

        #token = access["access_token"]
        # expires_in = access["expires_in"]

        print(user)

        #print("____________________________________")

        # github_user = yield self.oauth2_request(github_user_info_endpoint, access_token=token)

        #print(github_user)

        #("____________________________________")

        #if not github_user:
        #    return None

        #user = self.get_user(github_user)

        #return user
        return None

    @staticmethod
    def print_result(response):
        print(response.request.headers)
        print(response.body)

    def get_auth_http_client(self):
        http_headers = tornado.httputil.HTTPHeaders({"Accept": "application/json"})
        AsyncHTTPClient.configure(None, defaults=dict(headers=http_headers))
        return AsyncHTTPClient(defaults=dict(headers=http_headers))

    @tornado.gen.coroutine
    def handle_token_response(response):
        print(response.body)


    @staticmethod
    def get_user(google_user):

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

"""