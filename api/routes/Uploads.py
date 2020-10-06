import os
import uuid
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from api.Utils import authenticated
from api.model.models import User
from api.ImageUtils import resize_image

class PUTHandler(AuthenticatedHandler):
    @authenticated
    def post(self, user_name):

        session = self.settings['db']

        allowed_types = [
            {'type': 'image/jpeg', 'extension': '.jpg'},
            {'type': 'image/png', 'extension': '.png'}
        ]

        files = self.request.files
        file_name = ""

        # The user can only upload one avatar at a time.
        if len(files) > 1:
            response = {'Error': 'Only one avatar at at time can be uploaded to the server.'}
            self.set_status(413, "Error")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)
            return

        for field_name, files in files.items():
            for info in files:
                filename, content_type = info['filename'], info['content_type']

                filtered_type = [x for x in allowed_types if x['type'] == content_type]

                if len(filtered_type) is not 1:
                    response = {'Error': 'Only JPEG and PNG files are allowed.'}
                    self.set_status(400, "Error")
                    self.set_header("Access-Control-Allow-Origin", "*")
                    self.write(response)
                    return

                extension = filtered_type[0]['extension']
                save_name = user_name + "_" + str(uuid.uuid4())

                file_path = self.save_file(save_name, extension, info['body'])

                # Save user avatar.
                user = session.query(User).filter(User.username == user_name).one()

                old_avatar_name = user.avatar

                user.avatar = file_path
                session.commit()

                if old_avatar_name is not None:
                    self.delete_file(old_avatar_name)

        response = {'path': file_path}
        self.set_status(200, "Ok")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)
        return

    @staticmethod
    def save_file(name, extension, content):

        # Save image.
        filename = name + extension
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "static/avatars/") + filename
        with open(file_path, 'wb') as f:
            f.write(content)

        # Saved miniature size version.
        file_path_resized = os.path.join(current_dir, "static/avatars/") + "_reduced_" + filename
        resized = resize_image(file_path, 50, 50)
        resized.save(file_path_resized)

        return filename

    @staticmethod
    def delete_file(filename):
        current_dir = os.getcwd()
        path = os.path.join(current_dir, "static/avatars/") + filename
        os.remove(path)

    def options(self, user_name):
        response = {}
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.set_header("Accept", "multipart/form-data, '*'")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type,  X-Requested-With")
        self.set_header("Access-Control-Allow-Methods ", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_status(200, "Ok")
        self.write(response)

        return
