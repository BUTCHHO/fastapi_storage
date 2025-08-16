from fastapi import Request, Response, Query, Depends
from .schemas.query import AuthenticateQuery, SignUpQuery
from app.containers import Container
from dependency_injector.wiring import inject, Provide

from .router import auth_router



@auth_router.get('/_logout', name='auth-logout')
@inject
async def log_out_endpoint(
        response: Response,
        request: Request,
        logout_handler=Depends(Provide[Container.logout_handler])
        ):
    await logout_handler.logout_user(request=request, response=response)


@auth_router.post('/_sign-up', name='auth-sign_up')
@inject
async def sign_up_endpoint(
        params: SignUpQuery = Query(),
        sign_up_handler=Depends(Provide[Container.sign_up_handler])
        ):
    await sign_up_handler.sign_up(params)
    return {"message": 'successfully signed up'}

@auth_router.post('/_log-in', name='auth-login')
@inject
async def authenticate(
        response: Response,
        request: Request,
        params: AuthenticateQuery = Query(),
        auth_handler=Depends(Provide[Container.auth_handler])
        ):
    await auth_handler.auth_with_psw_and_set_session_cookie(params.name, params.password, response, request)
    return {"message": 'successfully logged_in'}






