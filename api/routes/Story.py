import json
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.model.models import Story
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from tornado.gen import coroutine


class StoryHandler(AuthenticatedHandler):

    def data_received(self, chunk):
        pass

    # GET /story/id
    def get(self, story_id):

        session = self.settings['db']

        try:
            story = session.query(Story).filter(Story.id == story_id).one()
            content = json.loads(story.content)

            if story.category is None:
                category = {'id': -1, 'name': "uncatalogued"}
            else:
                category = {'id': story.category.id, 'name': story.category.name}

            comments = []
            for comment in story.comments:
                json_comment = {
                     'id': comment.id,
                     'author': comment.author,
                     'content': comment.content,
                     'avatar': comment.avatar,
                     'date': str(comment.date),
                     'url': comment.url,
                }

                comments.append(json_comment)

            response = {
                 'id': story.id,
                 'title': story.title,
                 'category': category,
                 'content': content,
                 'date': str(story.date),
                 'comments': comments,
                 'tags': story.tags,
                 'is_draft': story.is_draft
            }

            status = 200
            status_str = 'Ok'

        except NoResultFound:
            status = 500
            status_str = "Error"
            response = {'message': 'No stories found for the specified id.'}

        except MultipleResultsFound:
            status = 500
            status_str = "error"
            response = {'message': 'Multiple stories found for the specified id.'}

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status, status_str)
        self.write(response)

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
