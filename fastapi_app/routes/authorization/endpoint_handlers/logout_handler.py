from fastapi import Request, Response

from auth.logouter import Logouter

class LogOutHandler:
    def __init__(self, user_logouter):
        self.logouter: Logouter = user_logouter

    async def logout_user(self, request: Request, response: Response):
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return
        await self.logouter.delete_session(session_id)
        response.delete_cookie('session_id')

