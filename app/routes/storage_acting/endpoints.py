from fastapi import Depends, Query, Request

from .schemas.query import MakeDirInStorageQuery, DeleteEntityQuery
from app.containers import Container
from dependency_injector.wiring import inject, Provide

from .router import storage_acting_router


@storage_acting_router.post('/make-dir-in-storage')
@inject
async def make_dir_in_storage(
        request: Request,
        auth_depend=Depends(Provide[Container.auth_depend]),
        params: MakeDirInStorageQuery = Query(),
        make_dir_handler=Depends(Provide[Container.make_dir_handler])
        ):
    user = await auth_depend.auth(request)
    make_dir_handler.make_dir_in_storage(user.storage_id, params.path_in_storage, params.name)

@storage_acting_router.delete('/delete-entity-in-storage')
@inject
async def delete_entity(
        request: Request,
        params: DeleteEntityQuery = Query(),
        delete_entity_handler=Depends(Provide[Container.delete_entity_handler]),
        auth_depend = Depends(Provide[Container.auth_depend])
        ):
    user = await auth_depend.auth(request)
    auth_depend.ask_for_password(params.password, user)
    delete_entity_handler.delete_entity(str(user.storage_id), params.path_in_storage)
