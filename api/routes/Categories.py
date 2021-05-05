import json
from api.model.models import Category, Story
from api.authentication.AuthenticatedHandler import AuthenticatedHandler
from tornado.web import RequestHandler
from tornado.gen import coroutine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.Utils import authenticated


class CategoryHandler(AuthenticatedHandler):

    def get(self, category_id):

        session = self.settings['db']
        category = session.query(Category).filter(Category.id == category_id).one()

        response = {
            'id': category.id,
            'name': category.name
        }

        self.set_status(200, 'Ok')
        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

        return

    @authenticated
    def delete(self, category_id):

        try:

            session = self.settings['db']
            category = session.query(Category).filter(Category.id == category_id).one()
            session.delete(category)
            session.commit()

            response = {'id': category_id}
            self.set_status(200, 'Ok')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        except NoResultFound:
            response = {'message': 'No result found for the specified id.'}
            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

        except MultipleResultsFound:

            response = {'message': 'Multiple categories found for the specified id.'}
            self.set_status(500, 'Error')
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(response)

            return

    @coroutine
    def options(self, id):
        response = {}
        self.set_header("Content-Type", "test/plain;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization")
        self.set_header("Access-Control-Allow-Methods ", "GET, POST, DELETE, OPTIONS")
        self.set_status(200, "Ok")
        self.write(response)

        return


class CategoryTopicsHandler(RequestHandler):

    def get(self, category_id, page):

        session = self.settings['db']

        if int(category_id) == -1:
            id_to_search = None
        else:
            id_to_search = int(category_id)

        category_stories = session.query(Story).filter(Story.category_id == id_to_search).all()
        data = []

        for story in category_stories:

            if story.category is None:
                category = {'id': -1, 'name': "uncatalogued"}
            else:
                category = {'id': story.category.id, 'name': story.category.name}

            json_item = {
                'id': story.id,
                'name': story.title,
                'title': story.title,
                'date': str(story.date),
                'comments': len(story.comments),
                'category': category,
                'author': {
                    'id': story.user.id,
                    'name': story.user.username,
                    'avatar': story.user.avatar
                }
            }

            data.append(json_item)

        response = {
            'currentPage': int(1),
            'totalPages': int(1),
            'items': data
        }

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)

    @coroutine
    def options(self, **id):
        response = {}
        self.set_header("Content-Type", "test/plain;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization")
        self.set_header("Access-Control-Allow-Methods ", "GET, POST, DELETE, OPTIONS")
        self.set_status(200, "Ok")
        self.write(response)

        return

class CategoriesHandler(AuthenticatedHandler):

    # GET /categories
    @coroutine
    def get(self):
        session = self.settings['db']
        all_categories = session.query(Category).all()

        data = []

        for category in all_categories:
            json_category = {
              'id': category.id,
              'name': category.name,
              'description': category.description,
            }

            data.append(json_category)

        response = {
            "page": 1,
            "items": data
        }

        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(response)
        return


    @coroutine
    def options(self, **id):
        response = {}
        self.set_header("Content-Type", "test/plain;charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization")
        self.set_header("Access-Control-Allow-Methods ", "GET, POST, DELETE, OPTIONS")
        self.set_status(200, "Ok")
        self.write(response)

        return

    # POST /categories
    @authenticated
    def post(self):

        request = self.request.body.decode("utf-8")
        json_request = json.loads(json.loads(request))
        name = json_request["name"]
        description = json_request["description"]

        category = Category()
        category.name = name
        category.description = description

        session = self.settings['db']
        session.add(category)
        session.commit()

        response = {'id': category.id, 'name': category.name, 'description': category.description}

        self.set_status(200, 'Ok')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/jsonp;charset=UTF-8")
        self.write(response)

        return
