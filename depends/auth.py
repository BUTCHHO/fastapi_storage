from fastapi import Request

from exceptions import APIUserDontExists
from exceptions.auth_http_exc import APIIncorrectPassword
from auth.exceptions import IncorrectPassword, UserDontExists
from exceptions.auth_http_exc import APIUnauthorized

class AuthDepend:
    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

    async def auth_allow_unauthorized(self, request: Request):
        try:
            return await self.auth(request)
        except APIUserDontExists:
            return None
        except APIUnauthorized:
            return None

    async def auth(self, request: Request):
        session_id = request.cookies.get('session_id')
        return await self.auth_handler.auth_with_session_id(session_id)

    def ask_for_password(self, password, user):
        try:
            self.auth_handler.check_password(password, user)
        except IncorrectPassword:
            raise APIIncorrectPassword
        except UserDontExists:
            raise APIUserDontExists('')
