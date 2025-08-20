from fastapi import Depends, Query, Request, Response

from .schemas.query import AccountDeleteQuery
from fastapi_app.containers import Container
from dependency_injector.wiring import inject, Provide

from .router import settings_router

#TODO need to delete or safe-delete user's storage


@settings_router.delete('/settings/delete_acc')
@inject
async def delete_user(request: Request,
                response: Response,
                params: AccountDeleteQuery = Query(),
                settings_handler=Depends(Provide[Container.settings_handler]),
                auth_depend=Depends(Provide[Container.auth_depend])
                ):
    user = await auth_depend.auth(request)
    auth_depend.ask_for_password(password=params.password, user=user)
    await settings_handler.delete_account(user.id, params.should_delete_storage, request, response)
    return {"message": 'account deleted'}

