from fastapi import APIRouter, Depends, Query, Request, Response

from ..dependencies import auth_depend
from .schemas.query import AccountDeleteQuery

from app.singletones import user_actor, logger, user_logouter, storage_deleter

from .endpoint_handlers import SettingsHandler

settings_router = APIRouter()

settings_handler = SettingsHandler(user_actor, logger, user_logouter, storage_deleter)

#TODO need to delete or safe-delete user's storage


@settings_router.delete('/settings/delete_acc')
async def delete_user(request: Request,
                response: Response,
                user=Depends(auth_depend.auth),
                params: AccountDeleteQuery = Query()):

    auth_depend.ask_for_password(password=params.password, user=user)
    await settings_handler.delete_account(user.id, params.should_delete_storage, request, response)
    return {"message": 'account deleted'}

