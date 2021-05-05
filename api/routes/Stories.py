import json
from api.model.models import Story, User, Category
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.Utils import authenticated
import datetime


class StoriesHandler(AuthenticatedHandler):
    def data_received(self, chunk):
        pass

    # GET /stories
    @coroutine
    def get(self):

        session = self.settings['db']
        story_id = self.get_argument("id", default=None)

        if story_id is not None:

            story = session.query(Story).filter(Story.id == story_id and Story.is_draft == False).one()

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
                    'url': comment.url,
                    'date': str(comment.date)
                }

                comments.append(json_comment)

            json_author = {
                'id': story.author.id,
                'name': story.author.fullname,
                'avatar': story.author.avatar,
                'username': story.author.username,
                'signature': story.author.signature
            }

            response = {
                'id': story.id,
                'title': story.title,
                'category': category,
                'content': story.content,
                'comments': comments,
                'tags': story.tags.split(','),
                'author': json_author,
                'date': str(story.date)
            }

            self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        else:
            # Hardcoded page page size. Move to configuration options.
            page_number = int(self.get_argument("page", default=0))
            PAGE_SIZE = 5
            OFFSET = PAGE_SIZE * page_number
            all_stories = session.query(Story).filter(Story.is_draft == False).order_by(Story.id.desc()).limit(PAGE_SIZE).offset(OFFSET)
            row_count = session.query(Story).count()
            data = []

            for story in all_stories:

                if story.category is None:
                    category = {'id': -1, 'name': "Uncategorized"}
                else:
                    category = {'id': story.category.id, 'name': story.category.name}

                json_story = {
                    'id': story.id,
                    'name': story.title,
                    'content': story.content,
                    'tags': story.tags.split(','),
                    'author': {
                        'id': story.user.id,
                        'name': story.user.username,
                        'avatar': story.user.avatar
                    },
                    'comments': len(story.comments),
                    'date': str(story.date),
                    'category': category
                }

                data.append(json_story)

            response = {
               "page": page_number,
               "items": data,
               "pageSize": PAGE_SIZE,
               "totalItems": row_count
            }

            self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        # POST /stories/new

    @authenticated
    def post(self):

        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))
        title = json_request["title"]
        tags = ",".join(json_request["tags"])
        content = json.dumps(json_request["content"])
        author_id = json_request["author"]
        category_id = json_request["category"]
        is_draft = json_request['is_draft']

        session = self.settings['db']

        try:
            category = session.query(Category).filter(Category.id == category_id).one()
        except NoResultFound:
            category = None

        story = self.save_story(session, content, title, author_id, category, tags, is_draft)

        if story.category is not None:
           category = {'id': story.category.id, 'name': story.category.name}
        else:
            category =  None

        json_story = {
            'id': story.id,
            'name': story.title,
            'content': story.content,
            'tags': story.tags.split(','),
            'author': {
                'id': story.user.id,
                'name': story.user.username,
                'avatar': story.user.avatar
            },
            'comments': [],
            'category': category,
            'date': str(story.date),
            'is_draft': str(is_draft)
        }

        self.set_status(200, 'Ok')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(json_story))


    # PUT /stories/:story_id
    @authenticated
    def put(self, story_id):

        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))
        content = json.dumps(json_request["content"])

        session = self.settings['db']

        category_id = json_request["category"]
        is_draft = json_request["is_draft"]

        try:
            category = session.query(Category).filter(Category.id == category_id).one()
        except NoResultFound:
            category = None

        try:

            tags = ",".join(json_request["tags"])

            story = session.query(Story).filter(Story.id == story_id).one()
            story.title = json_request["title"]
            story.content = str(content)
            story.tags = tags
            story.category = category
            story.is_draft = is_draft

            session.commit()
            status = 200
            status_str = 'Ok'
            response = {'id': story_id}

        except NoResultFound:
            status = 500
            status_str = "error"
            response = {'message': 'No story found for the specified id.'}

        except MultipleResultsFound:
            status = 500
            status_str = "error"
            response = {'message': 'Multiple stories found for the specified id.'}

        json.dumps(response)

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status, status_str)
        self.write(response)

        return

    @authenticated
    def delete(self, story_id):

        session = self.settings['db']

        try:

            story = session.query(Story).filter(Story.id == story_id).one()
            session.delete(story)
            session.commit()

            status = 200
            status_str = 'Ok'
            response = {'id': story_id}

        except NoResultFound:
            status = 500
            status_str = "error"
            response = {'message': 'No stories found for the specified id.'}

        except MultipleResultsFound:
            status = 500
            status_str = "error"
            response = {'message': 'Multiple Stories found for the specified id.'}

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_status(status, status_str)
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
        self.write(json.dumps(response))

        return

    @coroutine
    def options(self, *args):
        response = {}
        self.set_header("Content-Type", "test/plain;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization")
        self.set_header("Access-Control-Allow-Methods ", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_status(200, "Ok")
        self.write(response)

        return

    @coroutine
    def patch(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(response))

        return

    @coroutine
    def head(self):
        response = {"message": "This is not a valid method for this resource."}
        self.set_status(405, 'Error')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(response))

        return

    @staticmethod
    def save_story(session, content, title, author_id, category, tags, is_draft):

        user = session.query(User).filter(User.id == author_id).one()
        current_date = datetime.datetime.now()

        story = Story()
        story.title = title
        story.content = str(content)
        story.category = category
        story.user_id = author_id
        story.tags = tags
        story.date = current_date
        story.is_draft = is_draft
        user.stories.append(story)
        session.commit()

        return story


# TODO: integrate into stories handler.
class StoriesByUserHandler(RequestHandler):

    # GET /user/stories
    def get(self, user_id):

        session = self.settings['db']

        data = []

        # TODO: esto no siempre es verdadero.
        # Asumimos que el usuario siempre existe.
        user = session.query(User).filter(User.id == user_id).one()
        all_stories = user.stories

        for story in all_stories:

            if story.category is None:
                category = {'id': -1, 'name': "Uncategorized"}
            else:
                category = {'id': story.category.id, 'name': story.category.name}

            json_story = {
                'id': story.id,
                'name': story.title,
                'author': {
                    'id': user.id,
                    'name': user.username,
                    'avatar': user.avatar,
                    'signature': user.signature
                },
                'date': str(story.date),
                'comments': len(story.comments),
                'category': category
            }

            data.append(json_story)

        response = {"page": 1, "stories": data}

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)
