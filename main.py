import ssl
import tornado.web
from base64 import b64encode
from os import urandom, path
from api.AppRoutes import get_app_routes
from api.LoadOptions import load_options
from tornado.httpserver import HTTPServer
from api.model.sessionHelper import get_global_session
#from CachedHandler import CachedFileHandler

config_file = 'config.ini'
static_path = path.join(path.dirname(__file__), "static")

# Set application options
random_bytes = urandom(25)
secret = b64encode(random_bytes).decode('utf-8')

if __name__ == "__main__":

    # Set options.
    options = load_options(config_file)
    session_object = get_global_session(options)
    session = session_object()
    options['notification_handlers'] = dict([])
    options['db'] = session
    options['static_handler_class'] = 'CachedHandler'
    options['static_path'] = static_path

    routes = get_app_routes(static_path, options['notifications_enabled'])

    # Create application.
    application = tornado.web.Application(routes, **options)
    app_port = options["port"]

    if options['serve_https']:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(options['ssl_cert'], options['ssl_key'])
        server = HTTPServer(application, ssl_options=ssl_ctx)
    else:
        # Serve the application without HTTPS support (not recommended).
        server = HTTPServer(application)

    server.listen(app_port)
    tornado.ioloop.IOLoop.instance().start()
