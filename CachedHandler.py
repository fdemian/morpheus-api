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
