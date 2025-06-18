from interfaces import IModelReader
from exceptions import UserDontExists, IncorrectPassword, SessionExpired


class UserAuthentication:
    def __init__(self, user_reader, session_validator, session_maker, session_getter, logger, hasher):
        self.user_reader: IModelReader = user_reader
        self.session_maker = session_maker
        self.hasher = hasher
        self.logger = logger
        self.session_getter = session_getter
        self.session_validator = session_validator

    def get_user_with_name(self, name):
        return self.user_reader.get_by_kwargs(name=name)

    def is_password_correct(self, password, actual_password):
        return self.hasher.compare_psw_with_hash(password, actual_password)

    def authenticate_by_psw_and_return_session_id(self, name, password):
        try:
            user = self.get_user_with_name(name)
            if user is None:
                raise UserDontExists(name)
            if not self.is_password_correct(password, user.password):
                raise IncorrectPassword
            session = self.session_maker.create_session(user.id, user.name)
            return session.id
        except Exception as e:
            self.logger.log(e)

    def authenticate_by_session_id(self, session_id):
        return self.session_getter.get_user_by_session_id(session_id)
