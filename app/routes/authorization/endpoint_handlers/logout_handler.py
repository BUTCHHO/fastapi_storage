from fastapi import Request, Response

from exceptions.database_repo import FieldUniqueViolation
from auth.logouter import Logouter

class LogOutHandler:
    def __init__(self, user_logouter, logger):
        self.logouter: Logouter = user_logouter
        self.logger = logger

    async def logout_user(self, request: Request, response: Response):
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return
        try:
            await self.logouter.delete_session(session_id)
            response.delete_cookie('session_id')
        except FieldUniqueViolation:
            return
        except Exception as e:
            self.logger.log(e)
