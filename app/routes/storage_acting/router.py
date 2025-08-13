from aiofiles.threadpool.utils import delegate_to_executor
from fastapi import APIRouter, Depends, Query

from .schemas.query import MakeDirInStorageQuery, DeleteEntityQuery
from .endpoint_handlers import MakeDirHandler, DeleteEntityHandler
from app.containers import logger, storage_writer, path_joiner, path_ensurer
from app.routes.dependencies import auth_depend

storage_acting_router = APIRouter()

make_dir_handler = MakeDirHandler(logger, storage_writer, path_joiner, path_ensurer)
delete_entity_handler = DeleteEntityHandler(path_ensurer, storage_writer, path_joiner, logger)


@storage_acting_router.post('/make-dir-in-storage')
def make_dir_in_storage(user=Depends(auth_depend.auth), params: MakeDirInStorageQuery = Query()):
    make_dir_handler.make_dir_in_storage(user.storage_id, params.path_in_storage, params.name)

@storage_acting_router.delete('/delete-entity-in-storage')
def delete_entity(user=Depends(auth_depend.auth), params: DeleteEntityQuery = Query()):
    auth_depend.ask_for_password(params.password, user)
    delete_entity_handler.delete_entity(str(user.storage_id), params.path_in_storage)
