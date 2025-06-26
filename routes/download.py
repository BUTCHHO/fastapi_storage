from fastapi import APIRouter, BackgroundTasks, Query, Depends

from schemas.query import DownloadQuery
from view_handlers import FileResponseHandler
from app.singletones.singletones import archivator, logger, path_joiner, path_ensurer, storage_reader
from .dependencies import auth_depend

download_router = APIRouter()

file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer, path_joiner)



@download_router.get('/download-entity')
def download_entity_endpoint(background_tasks: BackgroundTasks, params: DownloadQuery = Query(), user=Depends(auth_depend.auth)):
    response = file_response_handler.get_response(user.id, params.entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response