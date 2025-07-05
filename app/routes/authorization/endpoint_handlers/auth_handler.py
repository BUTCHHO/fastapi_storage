from fastapi import Response, Request

from exceptions import APIIncorrectPassword, APIUserDontExists, \
    APISessionDontExists, APISessionExpired, APIUnauthorized
from auth.exceptions import SessionExpired, SessionDontExists, IncorrectPassword, UserDontExists
from config import SESSION_COOKIES_EXPIRE_TIME

class AuthHandler:
    def __init__(self, authenticator):
        self.authenticator = authenticator

    def set_session_id_cookie(self, session_id, response: Response):
        response.set_cookie(key="session_id", value=session_id, max_age=SESSION_COOKIES_EXPIRE_TIME,
                            samesite='lax', httponly=True)

    def check_password(self, password, user):
        self.authenticator.validate_user_and_password('', user, password)

    def auth_with_psw_and_set_session_cookie(self, name, password, response: Response, request: Request):
        try:
            if request.cookies.get('session_id'):
                return
            session_id = self.authenticator.auth_by_name_and_psw(name, password)
            self.set_session_id_cookie(session_id, response)
        except IncorrectPassword:
            raise APIIncorrectPassword(password)
        except UserDontExists:
            raise APIUserDontExists(name)

    def auth_with_session_id(self, session_id):
        try:
            if session_id is None:
                raise APIUnauthorized
            return self.authenticator.auth_by_session_id(session_id)
        except SessionExpired:
            raise APISessionExpired
        except SessionDontExists:
            raise APISessionDontExists
        except UserDontExists:
            raise APIUserDontExists


