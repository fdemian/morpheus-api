import json
from api.model.sessionHelper import get_session
from api.model.models import Story, Comment, Notification, User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from tornado.gen import coroutine
import datetime


class CommentsHandler(AuthenticatedHandler):

    def data_received(self, chunk):
        pass

    @coroutine
    def get(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    # POST /stories/id/comments
    def post(self, story_id):

        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))
               
        author_name = json_request["name"]
        content = json.dumps(json_request["content"])
        avatar = json_request["avatar"]
        author_url = json_request["url"]
        is_anonymous = json_request['anonymous']
        author = None
        current_date = datetime.datetime.now()


        try:
            session = self.settings['db']
            story = session.query(Story).filter(Story.id == story_id).one()
            comment = Comment()

            if is_anonymous:
              comment.author = author_name

            else:
              # TODO: validate user login.
              author = session.query(User).filter(User.username == author_name).one()
              story_author = session.query(User).filter(User.username == author.username).one()
              comment.author = author.username


            comment.content = content
            comment.avatar = ''
            comment.url = author_url
            comment.story_id = story.id
            comment.date = current_date
            session.add(comment)
            session.commit()

            json_comment = {
                'id': comment.id,
                'author': comment.author,
                'content': comment.content,
                'avatar': comment.avatar,
                'url': comment.url,
                'story': story.title,
                'date': str(comment.date),
                'storyId': story.id
            }

            # TODO: remove "author is not None". Its just there to temporarily fix notifications logic.
            if self.settings['notifications_enabled'] and author is not None:
                text = comment.author + " commented on " + story.title
                link = "/stories/" + str(story.id) + "/" + story.title

                notification_id = self.save_notification(session, author, "comment", text, link)
                self.notify_new_comment(text, link, notification_id, story_author.id)

            response = json_comment
            status = 200
            status_str = 'Ok'

        except NoResultFound:
            # User or story not found in database
            status = 500
            status_str = "Error"
            response = {'message': 'Story does not exist.'}

        except MultipleResultsFound:
            status = 500
            status_str = "Error"
            response = {'message': 'Multiple results found.'}

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status, status_str)
        self.write(response)

        return

    @coroutine
    def put(self):
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
        self.write(json.dumps(response))

        return

    @coroutine
    def connect(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @coroutine
    def options(self, id):
        response = {}
        self.set_header("Content-Type", "test/plain;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization")
        self.set_status(200, "Ok")
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

    def notify_new_comment(self, text, link, id, author_id):

        notifications_handler = self.settings['notification_handlers'][str(author_id)]

        # The story author is not online. There's no need to send a notification.
        if notifications_handler is None:
            return

        message = {
           'id': id,
           'type': "comment",
           'text': text,
           'link': link,
           'read': False
        }

        notifications_handler.write_message(json.dumps(message))

        return

    @staticmethod
    def save_notification(session, user, notification_type, text, link):

        notification_to_save = Notification()
        notification_to_save.user_id = user.id
        notification_to_save.type = notification_type
        notification_to_save.text = text
        notification_to_save.link = link
        notification_to_save.read = False

        session.add(notification_to_save)
        session.commit()

        return notification_to_save.id
