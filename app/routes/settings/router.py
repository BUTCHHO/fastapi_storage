from fastapi import APIRouter, Depends, Query

from ..dependencies import auth_depend
from .schemas.query import AccountDeleteQuery

settings_router = APIRouter()


@settings_router.delete('/settings/delete_acc')
def delete_account(user=Depends(auth_depend.auth), params: AccountDeleteQuery = Query()):
    auth_depend.ask_for_password(password=params.password, user=user)
    #TODO ушёл спать. НАДО доделать
    return {"message": 'not implemented'}
