from tornado.websocket import WebSocketHandler


class Notifications(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def initialize(self,):
        pass

    def open(self, id):
        self.settings['notification_handlers'][str(id)] = self

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("Closing websocket")
