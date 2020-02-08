import jwt
import re
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from os import path, getcwd
from api.model.models import User, UserActivation
from api.Crypto import hash_password
from time import sleep

import functools


def authenticated(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            response = {'Error': "Token is invalid."}
            self.set_status(401, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)
            
            return
        return method(self, *args, **kwargs)
    return wrapper


# Decode a JWT token and return the results.
def validate_token(jwt_token, secret, algorithm):
    try:
        if jwt_token is None:
            return None

        payload = jwt.decode(jwt_token, secret, algorithms=[algorithm])

        return payload

    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None


@coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)

    return response.body


# TODO is the extension always jpg?
@coroutine
def download_avatar(url, username):
    data = yield fetch_coroutine(url)

    current_dir = getcwd()
    output_file_name = path.join(current_dir, "static/avatars/") + username + ".jpg"
    save_file(output_file_name, data)

    return username + ".jpg"


def save_file(path, data):
    with open(path, "bw") as f:
        f.write(data)


def uglify_username(username):

    # Remove all non-word characters (everything except numbers and letters)
    username = re.sub(r"[^\w\s]", '', username)

    # Replace all runs of whitespace with a single dash
    username = re.sub(r"\s+", '-', username)

    return username


def get_oauth_settings(settings):

    settings = {
        "facebook":  {
            "key": settings["facebook_api_key"],
            "secret":  settings["facebook_api_secret"]
        },
        "google": {
            "key": settings["google_oauth_key"],
            "secret": settings["google_oauth_secret"]
        }
    }

    return settings

def do_save_user(user_to_save, session, *args, **kwargs):
    # TODO: document this.

    is_valid = kwargs.get('is_valid', None)

    user = User()
    user.username = user_to_save["username"]
    user.password = hash_password(user_to_save["password"])
    user.fullname = user_to_save["name"]
    user.email = user_to_save['email']
    user.failed_attempts = user_to_save['failed_attempts']

    if is_valid is None:
        user.valid = False
    else:
        if is_valid is True:
           user.valid = True

    user.valid = is_valid  # A user is not valid until his/her email has ben verified.
    user.avatar = None
    session.add(user)
    session.commit()

    return user

def save_activation_info(activation_code, user, session):
    # Save activation info.
    user_activation = UserActivation()
    user_activation.code = activation_code
    user_activation.user_id = user.id
    session.add(user_activation)
    session.commit()
    return

def delay_time(delay_per_try, tries):
    seconds = delay_per_try * tries
    sleep(seconds)
    return