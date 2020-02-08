import json
from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.model.models import GlobalConfiguration
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

class GlobalConfigurationHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    # GET /options
    @coroutine
    def get(self):

        try:
            session = self.settings['db']
            config_options = session.query(GlobalConfiguration).all()

            options = []
            for option in config_options:
               json_option = {
                  'key': option.key,
                  'value': option.value
               }

            options.append(json_option)
            response = {"page": 1, "options": options}

            self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        except Exception as e:
            print(e)
            response = {'message': "Could not read configuration options."}

            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

    @coroutine
    # TODO: this shit ain't secure. Authenticate user.
    def put(self):

        session = self.settings['db']
        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))

        config = session.query(GlobalConfiguration).filter(GlobalConfiguration.key == json_request['key']).one()
        config.value = str(json_request['value'])

        session.commit()

        response = {'message': "Config updated sucessfully."}
        self.set_status(200, 'Ok')
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
