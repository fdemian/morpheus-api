# Route imports
from api.routes.Stories import StoriesHandler
from api.routes.Stories import StoriesByUserHandler
from api.routes.Drafts import DraftsHandler, DraftsByUserHandler
from api.routes.Users import UsersHandler, UserHandler
from api.routes.Categories import CategoriesHandler, CategoryHandler, CategoryTopicsHandler
from api.routes.Index import IndexHandler
from api.routes.Comments import CommentsHandler
from api.routes.ConfigOptions import ConfigHandler
from api.routes.Notifications import Notifications
from api.routes.Alerts import AlertsHandler
from api.routes.Authentication import Authentication
from api.routes.Activation import UserActivationHandler
from api.routes.Account import AccountHandler
from api.routes.Logout import LogoutHandler
from api.routes.NotFound import NotFoundHandler
from api.routes.Uploads import PUTHandler
from api.routes.GlobalOptions import GlobalConfigurationHandler
from api.routes.GoogleOauth import GoogleAuthService

from tornado.web import StaticFileHandler

class CachedFileHandler(StaticFileHandler):

    @classmethod
    def set_headers(self):
        print(":::::")
        self.set_header("Cache-Control", "public, max-age=3100")
        self.set_header("X-Cache-Control", "public, max-age=3100")
        self.set_header("X-Pepocho", "0000")

    @classmethod
    def set_extra_headers(self):
        print(":::::")
        self.set_header("Cache-Control", "public, max-age=3100")
        self.set_header("X-Cache-Control", "public, max-age=3100")
        self.set_header("X-Pepocho", "0000")

    @classmethod
    def get_cache_time(self):
        print(":::::")
        return 31000


def get_app_routes(static_path, notifications_enabled):

    routes = [
       (r"/api/notifications/(.*)", Notifications),
       (r"/api/drafts/([0-9]+)", DraftsHandler),
       (r"/api/drafts", DraftsHandler),
       (r"/api/stories/([0-9]+)", StoriesHandler),
       (r"/api/stories", StoriesHandler),
       (r"/api/stories/(.*)/comments", CommentsHandler),
       (r"/api/options", GlobalConfigurationHandler),
       (r"/api/users/(.*)/stories", StoriesByUserHandler),
       (r"/api/users/(.*)/drafts", DraftsByUserHandler),
       (r"/api/users", UsersHandler),
       (r"/api/users/(.*)", UserHandler),
       (r"/api/account/(.*)", AccountHandler),
       (r"/api/categories/([-1-9]+)", CategoryHandler),
       (r"/api/categories/([-1-9]+)/([-1-9]+)", CategoryTopicsHandler),
       (r"/api/categories", CategoriesHandler),
       (r"/api/oauth/google/(.*)", GoogleAuthService),
       (r"/api/auth", Authentication),
       (r"/api/auth/logout/", LogoutHandler),
       (r"/api/config",  ConfigHandler),
       (r"/api/activation", UserActivationHandler),
       (r"/api/alerts", AlertsHandler),
       (r"/api/alerts/", AlertsHandler),
       (r"/api/uploads/(.*)", PUTHandler),
       #(r"/api/uploads", UploadHandler),
       #(r"/api/uploads", UploadHandler),
       # (r"/api/uploads/(.*)", PUTHandler),
       (r"/api/(.*)", NotFoundHandler),
       #(r'/(.*)', CachedFileHandler, {'path': static_path, 'default_filename':'index.html'}),
       #(r"/(manifest\.json)", AlertsHandler, {"path": static_path}),
       #(r"/(favicon\.png)", AlertsHandler, {"path": static_path}),
       #(r"/(robots\.txt)", AlertsHandler, {"path": static_path}),
       #(r"/static/(.*)", CachedFileHandler, {"path": static_path}),
       #(r"/.*", IndexHandler)
    ]

    return routes
