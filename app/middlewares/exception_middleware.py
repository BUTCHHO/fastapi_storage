import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from exceptions import APIUnsupportedEntityType
from exceptions.auth_http_exc import APIUnauthorized, APISessionExpired, APISessionDontExists, APIUserDontExists, APIUserAlreadyExists, APIIncorrectPassword
from exceptions.http_files_exc import APITooManyFiles
from exceptions.path_http_exc import APIEntityDoesNotExists, APIEntityIsNotADir,APIDirectoryAlreadyExists,APIUserStorageAlreadyExists,APIPathGoesBeyondLimits
from auth.exceptions import Unauthorized, SessionExpired, SessionDontExists, UserDontExists, UserAlreadyExists, IncorrectPassword
from exceptions.path_exc import EntityDoesNotExists,UnsupportedEntityType, TooManyFiles,  EntityIsNotADir, PathGoesBeyondLimits, UserStorageAlreadyExists, DirectoryAlreadyExists



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
            UnsupportedEntityType: APIUnsupportedEntityType,
        }
        self.logger = logging.getLogger(__name__)
        super().__init__(app, dispatch)

    def return_error_json_response(self, exception):
            exception_type = type(exception)
            try:
                http_exc = self.mapper[exception_type]()
            except KeyError:
                return self.log_error_and_return_500_error()
            return self.make_json_response(status_code=http_exc.status_code, detail=http_exc.detail)


    def make_json_response(self, status_code, detail):
        return JSONResponse(status_code=status_code, content={'detail': detail})

    def log_error_and_return_500_error(self):
        self.logger.exception('KEY ERROR')
        return self.make_json_response(500, 'internal server error')


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
        except Exception as e:
            response = self.return_error_json_response(e)
        return response

#здесь пропадает какой либо смысл использовать HTTPException. статус код и детали можно хранить в обычном Exception питона



