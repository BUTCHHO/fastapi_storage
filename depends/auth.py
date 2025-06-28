from fastapi import Request
from exceptions.auth_http_exc import APIIncorrectPassword, APIUserDontExists
from exceptions.auth import IncorrectPassword, UserDontExists

class AuthDepend:
    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

    def auth(self, request: Request):
        session_id = request.cookies.get('session_id')
        return self.auth_handler.auth_with_session_id(session_id)

    def ask_for_password(self, password, user):
        try:
            self.auth_handler.check_password(password, user)
        except IncorrectPassword:
            raise APIIncorrectPassword
        except UserDontExists:
            raise UserDontExists('')
