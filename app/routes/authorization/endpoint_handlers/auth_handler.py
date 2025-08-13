from fastapi import Response, Request

from auth.authentication import Authenticator

from exceptions import APIIncorrectPassword, APIUserDontExists, \
    APISessionDontExists, APISessionExpired, APIUnauthorized
from auth.exceptions import IncorrectPassword, UserDontExists, SessionDontExists, SessionExpired

class AuthHandler:
    def __init__(self, authenticator, session_cookies_expire_time):
        self.authenticator: Authenticator = authenticator
        self.SESSION_COOKIES_EXPIRE_TIME = session_cookies_expire_time

    def set_session_id_cookie(self, session_id, response: Response):
        response.set_cookie(key="session_id", value=session_id, max_age=self.SESSION_COOKIES_EXPIRE_TIME,
                            samesite='lax', httponly=True)

    def check_password(self, password, user):
        self.authenticator.check_password(password, user.password)

    async def auth_with_psw_and_set_session_cookie(self, name, password, response: Response, request: Request):
        try:
            session_id = await self.authenticator.auth_by_name_and_psw_and_return_session_id(name, password)
            self.set_session_id_cookie(session_id, response)
        except IncorrectPassword:
            raise APIIncorrectPassword()
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

#TODO когда в бд нету сессии, а у юзера в куки она есть, то при попытке аутентификации пробивается 500 error из за auth.exceptions.SessionDontExists
# я хз как это исправить и почему исключение не ловится

