from tornado.websocket import WebSocketHandler


class Notifications(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def initialize(self):
        print("initialize");
        self.settings['notifications_handler'] = self

    def open(self):
        print("initialize");
        self.settings['notifications_handler'] = self

    # Notifications for a given user were requested.
    def on_message(self, message):
        print(message)

    def on_close(self):
        print("Closing websocket")
