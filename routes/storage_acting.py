from fastapi import APIRouter, Depends, Query

from schemas.query import MakeDirInStorageQuery
from view_handlers import MakeDirHandler
from app.singletones.singletones import logger, storage_writer, path_joiner, path_ensurer
from .dependencies import auth_depend

storage_acting_router = APIRouter()

make_dir_handler = MakeDirHandler(logger, storage_writer, path_joiner, path_ensurer)



@storage_acting_router.post('/make-dir-in-storage')
def make_dir_in_storage(user=Depends(auth_depend.auth), params: MakeDirInStorageQuery = Query()):
    make_dir_handler.make_dir_in_storage(user.id, params.path_in_storage, params.name)