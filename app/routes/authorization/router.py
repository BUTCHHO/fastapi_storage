from fastapi import APIRouter, Request, Response, Query
from .endpoint_handlers import SignUpHandler, LogOutHandler, AuthHandler
from app.singletones import session_deleter, logger, user_reader, storage_writer, user_registrator, user_authenticator
from .schemas.query import AuthenticateQuery, SignUpQuery


auth_router = APIRouter()


logout_handler = LogOutHandler(session_deleter, logger)
sign_up_handler = SignUpHandler(user_registrator, storage_writer, user_reader)
auth_handler = AuthHandler(user_authenticator)


@auth_router.post('/log-out')
def log_out_endpoint(request: Request, response: Response):
    logout_handler.logout_user(request, response)


@auth_router.post('/sign-up')
def sign_up_endpoint(params: SignUpQuery = Query()):
    sign_up_handler.sign_up(params)
    return {"message": 'successfully signed up'}

@auth_router.post('/log-in')
def authenticate(response: Response, params: AuthenticateQuery = Query()):
    auth_handler.auth_with_psw_and_set_session_cookie(params.name, params.password, response)
    return {"message": 'successfully logged_in'}

from jinja2




