from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from exceptions.auth_http_exc import APIUnauthorized, APISessionExpired, APISessionDontExists, APIUserDontExists, APIUserAlreadyExists, APIIncorrectPassword
from exceptions.http_files_exc import APITooManyFiles
from exceptions.path_http_exc import APIEntityDoesNotExists, APIEntityIsNotADir,APIDirectoryAlreadyExists,APIUserStorageAlreadyExists,APIPathGoesBeyondLimits
from auth.exceptions import Unauthorized, SessionExpired, SessionDontExists, UserDontExists, UserAlreadyExists, IncorrectPassword
from exceptions.path_exc import EntityDoesNotExists, TooManyFiles,  EntityIsNotADir, PathGoesBeyondLimits, UserStorageAlreadyExists, DirectoryAlreadyExists



class ExceptionCatcherMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        self.mapper = {
            Unauthorized: APIUnauthorized,
            SessionExpired: APISessionExpired,
            SessionDontExists: APISessionDontExists,
            UserDontExists: APIUserDontExists,
            UserAlreadyExists: APIUserAlreadyExists,
            IncorrectPassword: APIIncorrectPassword,
            TooManyFiles: APITooManyFiles,
            EntityIsNotADir: APIEntityIsNotADir,
            PathGoesBeyondLimits: APIPathGoesBeyondLimits,
            EntityDoesNotExists: APIEntityDoesNotExists,
            DirectoryAlreadyExists: APIDirectoryAlreadyExists,
            UserStorageAlreadyExists: APIUserStorageAlreadyExists,
        }
        super().__init__(app, dispatch)
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            exception_type = type(e)
            try:
                http_exc = self.mapper[exception_type]()
                return JSONResponse(status_code=http_exc.status_code, content={'detail':http_exc.detail})
            except KeyError:
                print('CAUGHT KEY ERROR')
                raise



