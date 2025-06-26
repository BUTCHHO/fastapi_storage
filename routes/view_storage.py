from fastapi import APIRouter, Depends
from app.singletones.singletones import storage_reader, logger, path_joiner, path_cutter, path_ensurer
from schemas.response import ViewStorageResponse
from view_handlers import StorageViewHandler
from .dependencies import auth_depend

view_storage_router = APIRouter()

storage_view_handler = StorageViewHandler(storage_reader, logger, path_joiner, path_cutter, path_ensurer)


@view_storage_router.get('/storage', response_model=ViewStorageResponse)
def view_storage_root(entity_path_in_storage = '', user=Depends(auth_depend.auth)):
    entities = storage_view_handler.get_list_of_entities(user.id, entity_path_in_storage)
    return {"entities": entities}


@view_storage_router.get('/storage/{entity_path_in_storage:path}', response_model=ViewStorageResponse)
async def view_storage(entity_path_in_storage: str, user=Depends(auth_depend.auth)):
    entities = storage_view_handler.get_list_of_entities(user.id, entity_path_in_storage)
    return {"entities": entities}