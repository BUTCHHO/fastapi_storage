from fastapi import Request, Response

from exceptions.database_repo import FieldUniqueViolation


class LogOutHandler:
    def __init__(self, user_logouter, logger):
        self.logouter = user_logouter
        self.logger = logger

    def logout_user(self, request: Request, response: Response):
        try:
            self.logouter.logout_user(request, response)
        except FieldUniqueViolation:
            return
        except Exception as e:
            self.logger.log(e)
