from exceptions.database_repo import FieldUniqueViolation
from interfaces import IModelReader
from .exceptions import UserDontExists, IncorrectPassword, SessionDontExists, SessionExpired


class UserAuthentication:
    def __init__(self, user_reader, session_getter, session_maker, user_getter, logger, hasher):
        self.user_reader: IModelReader = user_reader
        self.session_maker = session_maker
        self.hasher = hasher
        self.logger = logger
        self.user_getter = user_getter
        self.session_getter = session_getter


    def _get_user_by_name(self, name):
        return self.user_reader.get_by_kwargs(name=name)

    def validate_user_and_password(self, user_name, user, psw):
        if not user:
            raise UserDontExists(user_name)
        if not self.hasher.check_password(psw, user.password):
            raise IncorrectPassword

    def _get_session_by_user_id(self, user_id):
        return self.session_getter.get_session_id_by_user_id(user_id)


    def auth_by_name_and_psw(self, name, psw):
        user = self._get_user_by_name(name)
        if user is None:
            raise UserDontExists
        self.validate_user_and_password(name, user, psw)
        try:
            return self._get_session_by_user_id(user.id)
        except SessionDontExists or SessionExpired:
            return self.session_maker.make_session(user.id)

    def auth_by_session_id(self, session_id):
        return self.user_getter.get_user_by_session_id(session_id)


