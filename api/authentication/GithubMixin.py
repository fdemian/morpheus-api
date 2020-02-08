#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import urllib.parse as urllib_parse

from tornado.concurrent import return_future
from tornado.auth import _auth_return_future, AuthError
from tornado import httpclient
from tornado.httputil import url_concat
from tornado import escape


class GithubOAuth2Mixin(object):
    _OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    _OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    _OAUTH_USER_BASE_URL = "https://api.github.com"
    _OAUTH_SETTINGS_KEY = "github_oauth"

    @return_future
    def authorize_redirect(self, scopes=None, response_type="code", callback=None, **kwargs):
        args = {
            "client_id": self.settings[self._OAUTH_SETTINGS_KEY]["key"],
            "response_type": response_type
        }
        if kwargs:
            args.update(kwargs)
        if scopes:
            args["scope"] = ",".join(scopes)
        self.redirect(
            url_concat(self._OAUTH_AUTHORIZE_URL, args))
        callback()

    @_auth_return_future
    def get_authenticated_user(self, code, callback):
        """Handles the login for the Github user, returning a user object.
        Example usage::
            class GithubOAuth2LoginHandler(tornado.web.RequestHandler,
                                           GithubOAuth2Mixin):
                @tornado.gen.coroutine
                def get(self):
                    if self.get_argument("code", False):
                        user = yield self.get_authenticated_user(code=self.get_argument("code"))
                        # Save the user with e.g. set_secure_cookie
                    else:
                        yield self.authorize_redirect(scope=["user:email"])
        """
        http = self.get_auth_http_client()
        body = urllib_parse.urlencode({
            "code": code,
            "client_id": self.settings[self._OAUTH_SETTINGS_KEY]["key"],
            "client_secret": self.settings[self._OAUTH_SETTINGS_KEY]["secret"],
        })

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                   functools.partial(self._on_access_token, callback),
                   method="POST",
                   headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
                   body=body)

    def _on_access_token(self, future, response):
        """Callback function for the exchange to the access token."""
        if response.error:
            future.set_exception(AuthError("Github auth error: %s" % str(response)))
            return

        args = escape.json_decode(escape.native_str(response.body))
        access_token = args.get("access_token", None)
        if not access_token:
            future.set_result(None)
        scopes = args["scope"].split(",")
        has_user_email_scope = scopes.count("user:email") > 0
        self.github_request(
            path="/user",
            callback=functools.partial(
                self._on_get_user_info, future, access_token, has_user_email_scope),
            access_token=access_token
        )

    def _on_get_user_info(self, future, access_token, has_user_email_scope, user):
        if user is None:
            future.set_result(None)
            return

        user.update({"access_token": access_token})
        if not has_user_email_scope:
            return future.set_result(user)
        self.github_request(
            path="/user/emails",
            callback=functools.partial(
                self._on_get_user_email, future, user),
            access_token=access_token
        )

    @staticmethod
    def _on_get_user_email(future, user, emails):
        user.update({"private_emails": emails})
        future.set_result(user)

    @_auth_return_future
    def github_request(self, path, callback, access_token=None, post_args=None, **args):
        url = self._OAUTH_USER_BASE_URL + path
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
        if all_args:
            url += "?" + urllib_parse.urlencode(all_args)
        callback = functools.partial(self._on_github_request, callback)
        http = self.get_auth_http_client()
        ua = "tornado"
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback, user_agent=ua,
                       headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"})
        else:
            http.fetch(url, method="GET", callback=callback, user_agent=ua, headers={"Accept": "application/json"})

    @staticmethod
    def _on_github_request(future, response):
        if response.error:
            future.set_exception(AuthError("Error response %s fetching %s" %
                                           (response.error, response.request.url)))
            return

        future.set_result(escape.json_decode(response.body))

    @staticmethod
    def get_auth_http_client():
        return httpclient.AsyncHTTPClient()

"""

    return arglist


class GithubOAuth2Mixin(tornado.auth.OAuth2Mixin):
    Github authentication using the new Graph API and OAuth2.
    _OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token?"
    _OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize?"
    _OAUTH_NO_CALLBACKS = False
    _API_URL = "https://api.github.com"

    # noinspection PyProtectedMember,PyIncorrectDocstring
    @tornado.auth._auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        fields = {'id', 'name', 'first_name', 'last_name', 'locale', 'picture', 'link', 'email'}
        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._oauth_request_token_url(**args),
                   functools.partial(self._on_access_token, redirect_uri, client_id,
                                     client_secret, callback, fields))

    # noinspection PyUnusedLocal
    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):

        if response.error:
            future.set_exception(tornado.auth.AuthError('Github auth error: %s' % str(response)))
            return

        parsed_url = urlparse(tornado.escape.native_str(response.body))
        parsed_list = parsed_url.path.split("&")

        session = {"access_token": parsed_list[0].split("=")[1]}

        print(session["access_token"])
        print(":__________________________________")


        self.github_request(
            path="/user",
            callback=functools.partial(
                self._on_get_user_info, future, session, fields),
            access_token=session["access_token"],
            fields=",".join(fields)
        )

    # noinspection PyMethodMayBeStatic
    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return


        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update({"access_token": session["access_token"], "session_expires": session.get("expires")})
        future.set_result(fieldmap)

    # noinspection PyProtectedMember,PyIncorrectDocstring
    @tornado.auth._auth_return_future
    def github_request(self, path, callback, access_token=None,
                       post_args=None, **args):

        url = self._API_URL + path
        oauth_future = self.oauth2_request(url, access_token=access_token,
                                           post_args=post_args, **args)
        tornado.concurrent.chain_future(oauth_future, callback)
"""