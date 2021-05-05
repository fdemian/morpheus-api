from tornado.web import RequestHandler
from os.path import isfile

class IndexHandler(RequestHandler):

    # GET
    def get(self):
        index_dir = "../../static/index.html"
        self.render(index_dir)

    def set_headers(self, path):
        print("this shoudl only be visible once")
        self.set_header('Cache-Control', 'public, max-age=31536000')
        self.set_header('X-Cache-Control', 'public, max-age=31536000')
        self.set_header('X-TEST', 'testestestestestetsestetset')
