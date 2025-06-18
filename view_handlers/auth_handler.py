from fastapi import Cookie

from exceptions import IncorrectPassword, UserDontExists


class UserAuthenticateHandler:
    def __init__(self, user_getter, session_validator, session_maker, cache_handler, authenticator):
        self.user_getter = user_getter
        self.session_validator = session_validator
        self.session_cacher = cache_handler
        self.session_maker = session_maker
        self.authenticator = authenticator

    def auth_and_ret_session_cookie(self, name, password):
        try:
            session_id = self.authenticator.authenticate_and_return_session_id(name, password)
        except IncorrectPassword:
            raise APIInorrectPassword
        except UserDontExists:
            raise APIUserDontExists

