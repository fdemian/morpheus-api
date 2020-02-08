from tornado.web import RequestHandler
from os.path import isfile

class IndexHandler(RequestHandler):

    # GET
    def get(self):
        index_dir = "../../static/index.html"
        self.render(index_dir)
