from fastapi import Request


class AuthDepend:
    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

    def auth(self, request: Request):
        session_id = request.cookies.get('session_id')
        return self.auth_handler.auth_with_session_id(session_id)
