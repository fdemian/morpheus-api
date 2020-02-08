import json
from api.model.models import Notification
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from tornado.gen import coroutine
from api.Utils import authenticated


class AlertsHandler(AuthenticatedHandler):

    def data_received(self, chunk):
        pass

    # GET /alerts
    @authenticated
    def get(self):

        if not self.settings['notifications_enabled']:
            response = {'message': "Notifications disabled."}
            self.set_status(501, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        session = self.settings['db']
        current_user = self.current_user
        
        alerts = session.query(Notification).filter(Notification.user_id == current_user, Notification.read == False)\
                        .order_by(Notification.id.desc())\
                        .all()

        data = []

        for notification in alerts:
            json_notification = {
                'id': notification.id,
                'type': notification.type,
                'text': notification.text,
                'link': notification.link,
                'read': notification.read
            }

            data.append(json_notification)

        response = {"notifications": data}

        self.set_status(200, 'Ok ')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    # TODO: change to POST method?
    #  -- REASON: Successful response returns a body (and shouldn't).
    #  -- Otherwise the method is same as PUT.
    # PUT /alerts
    @authenticated
    def put(self):

        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))

        session = self.settings['db']

        try:
            notification_id = int(json_request["id"])
            notification = session.query(Notification).filter(Notification.id == notification_id).one()

            # Modify all the fields.
            notification.type = json_request["type"]
            notification.text = json_request["text"]
            notification.link = json_request["link"]
            notification.read = json_request["read"]

            session.commit()

            status = 200
            status_str = 'Ok'
            response = {'id': notification_id}

        except NoResultFound:
            status = 500
            status_str = "Error"
            response = {'message': 'No notifications with the id' + notification_id + 'found.'}

        except MultipleResultsFound:
            status = 500
            status_str = "Error"
            response = {'message': 'More than one notification with the id' + notification_id + ' was found.'}

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status, status_str)
        self.write(response)

        return

    @coroutine
    def post(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def delete(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def trace(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def connect(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def options(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def patch(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def head(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return
