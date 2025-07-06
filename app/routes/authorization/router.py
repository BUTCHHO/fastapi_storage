from fastapi import APIRouter, Request, Response, Query
from .endpoint_handlers import SignUpHandler, LogOutHandler, AuthHandler
from app.singletones import user_logouter, logger, user_reader, storage_writer, user_registrator, user_authenticator
from .schemas.query import AuthenticateQuery, SignUpQuery


auth_router = APIRouter()


logout_handler = LogOutHandler(user_logouter, logger)
sign_up_handler = SignUpHandler(user_registrator, storage_writer, user_reader)
auth_handler = AuthHandler(user_authenticator)


@auth_router.get('/_logout', name='auth-logout')
async def log_out_endpoint(request: Request, response: Response):
    await logout_handler.logout_user(request, response)


@auth_router.post('/_sign-up', name='auth-sign_up')
def sign_up_endpoint(params: SignUpQuery = Query()):
    sign_up_handler.sign_up(params)
    return {"message": 'successfully signed up'}

@auth_router.post('/_log-in', name='auth-login')
async def authenticate(response: Response, request: Request, params: AuthenticateQuery = Query()):
    await auth_handler.auth_with_psw_and_set_session_cookie(params.name, params.password, response, request)
    return {"message": 'successfully logged_in'}


@auth_router.get('/profile', name='view-profile')
def view_profile():
    return {"message": 'not implemented'}

@auth_router.get('/log-in', name='view-login')
def view_login():
    return {"message": 'not implemented'}

@auth_router.get('/sign-up', name='view-sign_up')
def view_sign_up():
    return {"message": 'not implemented'}




