from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from exceptions.auth_http_exc import APIUnauthorized, APISessionExpired, APISessionDontExists, APIUserDontExists, APIUserAlreadyExists, APIIncorrectPassword
from exceptions.http_files_exc import APITooManyFiles
from exceptions.path_http_exc import APIEntityDoesNotExists, APIEntityIsNotADir,APIDirectoryAlreadyExists,APIUserStorageAlreadyExists,APIPathGoesBeyondLimits
from auth.exceptions import Unauthorized, SessionExpired, SessionDontExists, UserDontExists, UserAlreadyExists, IncorrectPassword
from exceptions.path_exc import EntityDoesNotExists, TooManyFiles,  EntityIsNotADir, PathGoesBeyondLimits



class ExceptionCatcherMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print('here is EXCEPTIONS', type(e))
