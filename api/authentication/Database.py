from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from api.model.models import User, UserActivation
from api.Crypto import hash_password, check_password
from api.Utils import  delay_time
import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseAuthService:

    def authenticate_user(self, username, password, settings):

        password_is_correct = False
        session = settings['db']
        user = self.get_user_if_exists(session, username)

        max_login_tries = settings['max_login_tries']
        login_delay = settings['login_delay_time_step']
        lockout_time = settings['lockout_time_window']

        if user is None:
            logger.info("Requested unexistent user: "  + username)
            user = self.get_mock_user()
            hash_password(user.password)
            user_exists = False
        else:
            logger.info("User exists and is: "  + username)
            logger.info(user.failed_attempts)
            user_exists = True
            delay_time(login_delay, user.failed_attempts) # Wait an ammount of time proportional to the number of failed attempts.

        check_pass = check_password(password, user.password)

        # User tried to login the maximum number of allowed tries.
        if self.user_is_locked(session, user, lockout_time):
            logger.info("User is locked: " + username)
            return None

        """
          If the user is valid and it exists verify that the password was input correctly.
          If not, register the failed attempt in the database.
        """
        if user.valid and user_exists:
            logger.info("User is valid and exists: ")
            if check_pass:
               password_is_correct = True
            else:
               logger.info("User is invalid or does not exist. ")
               password_is_correct = False
               self.register_failed_login(session, user, max_login_tries)
        else:
            password_is_correct = False

        if password_is_correct:
            logger.info("Password is correct. ")
            user_dict = self.user_to_dict(user)
            return user_dict
        else:
            return None

    @staticmethod
    def user_to_dict(user):

        user_link = '/users/' + str(user.id) + "/" + user.username

        payload = {
            'id': user.id,
            'avatar': user.avatar,
            'username': user.username,
            'fullname': user.fullname,
            'email': user.email,
            'role': 'author',
            'link': user_link,
            'signature': user.signature,
            'about': user.about
        }

        return payload

    @staticmethod
    def get_user_if_exists(session, username):
        try:
            user = session.query(User).filter(User.username == username).one()
            return user

        except MultipleResultsFound:
            return None

        except NoResultFound:
            return None

    @staticmethod
    def user_is_locked(session, user, lockout_time):

        if user.lockout_time is None:
            return False

        time_elapsed = datetime.datetime.now() - user.lockout_time
        if time_elapsed > lockout_time:
            user.lockout_time = None
            session.merge(user)
            session.commit()
            return False
        else:
            return True

    @staticmethod
    def unlock_user(session, user):
        user.failed_attempts=0
        user.lockout_time=None
        session.merge(user)
        session.commit()

    @staticmethod
    def register_failed_login(session, user, max_login_tries):
        user.failed_attempts = user.failed_attempts + 1

        # If the user reached the maximum number of tries.
        if user.failed_attempts is max_login_tries :
            user.lockout_time = datetime.datetime.now()

        session.merge(user)
        session.commit()

        return user

    def register_user(self, session, user_to_save, activation_code, *args, **kwargs):

        user_to_check = self.get_user_if_exists(session, user_to_save["username"])

        # If there is already a user with the same username, return.
        if user_to_check is not None:
            return None

        is_valid = kwargs.get('is_valid', None)

        print(user_to_save)

        # Save user.
        user = User()
        user.username = user_to_save["username"]
        user.password = hash_password(user_to_save["password"])
        user.fullname = ""
        user.email = user_to_save['email']
        user.failed_attempts = 0
        user.valid = is_valid
        user.avatar = ""
        session.add(user)
        session.commit()

        #Save activation info.
        if not is_valid:
            activation = UserActivation()
            activation.user = user
            activation.code = activation_code
            session.add(activation)
            session.commit()


        return user


    @staticmethod
    def get_mock_user():
        mock_user = User()
        mock_user.username = "fakeuser"
        mock_user.password = "fake_password"
        mock_user.lockout_time = datetime.datetime.now()
        mock_user.failed_attempts = 0
        mock_user.email = "fake@fake.com"
        mock_user.fullname = "Fake Mega User"
        mock_user.valid = False

        return mock_user

