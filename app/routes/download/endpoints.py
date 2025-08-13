from fastapi import BackgroundTasks, Request, Depends, Query

from .schemas.query import DownloadQuery
from app.containers import Container
from dependency_injector.wiring import inject, Provide

from .router import download_router

@download_router.get('/download-entity')
@inject
async def download_entity_endpoint(
        request: Request,
        background_tasks: BackgroundTasks,
        params: DownloadQuery = Query(),
        auth_depend=Depends(Provide[Container.auth_depend]),
        file_response_handler=Depends(Provide[Container.file_response_handler]),
        archivator=Depends(Provide[Container.archivator])
        ):
    user = await auth_depend.auth(request)
    response = file_response_handler.get_response(user.storage_id, params.entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response