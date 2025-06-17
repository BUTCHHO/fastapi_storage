from interfaces import IModelReader
from exceptions import UserDontExists, IncorrectPassword, SessionExpired


class UserAuthentication:
    def __init__(self, user_reader, session_validator, session_maker, session_getter, logger, password_check_func):
        self.user_reader: IModelReader = user_reader
        self.session_maker = session_maker
        self.password_check_func = password_check_func
        self.logger = logger
        self.session_getter = session_getter
        self.session_validator = session_validator

    def get_user_with_name(self, name):
        return self.user_reader.get_by_kwargs(name=name)

    def is_password_correct(self, password, actual_password):
        return self.password_check_func(password, actual_password)

    def authenticate_and_return_session(self, name, password):
        try:
            user = self.get_user_with_name(name)
            if user is None:
                raise UserDontExists(name)
            if not self.is_password_correct(password, user.password):
                raise IncorrectPassword
            self.session_maker.create_session(user.id, user.name)
            session = self.session_getter.get_session_by_user_id(user.id)
            return session.id
        except Exception as e:
            self.logger.log(e)


    def get_user(self, session):
        try:
            if self.session_validator.check_if_session_expired(session.expire_date):
                raise SessionExpired
            return self.user_reader.get_by_id(session.user_id)
        except Exception as e:
            self.logger.log(e)
