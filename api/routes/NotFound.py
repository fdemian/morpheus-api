from tornado.web import RequestHandler
from tornado.gen import coroutine


class NotFoundHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    @coroutine
    def get(self, args):
        msg = 'The requested route (' + args + ') was not found on the server.'
        response = {'message': msg}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def put(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def delete(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def trace(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def connect(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def options(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def patch(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def head(self):
        response = {'message': 'The route you were looking for was not found.'}
        self.set_status(404, 'NotFound')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return
