import json
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from api.model.models import User
from api.Crypto import check_password, hash_password

# TODO: integrate GET  in USERSHANDLER.
class AccountHandler(AuthenticatedHandler):

    # PUT /acccount/id
    def put(self, user_id):

        session = self.settings['db']
        request = self.request.body.decode("utf-8")

        user = session.query(User).filter(User.id == user_id).one()
        json_request = json.loads(request)

        password = json_request["password"]
        new_password = json_request["newpass"]
        response_msg = 'Ok'

        if (password is None) or (new_password is None):

            if password is None:
                response_msg = "Current password not specified"
            else:
                response_msg = "New password not specified"

            self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_status(500, 'Error')
            self.write({'Error': response_msg})

            return

        if check_password(password, user.password):
            user.password = hash_password(new_password)

        else:
            self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_status(500, 'Error')
            self.write({'Error': 'Wrong password specified.'})

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(200, 'Ok')
        self.write({'status': response_msg})

        return