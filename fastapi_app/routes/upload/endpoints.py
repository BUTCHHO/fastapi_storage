from fastapi import UploadFile, Query, Depends, Request
from .schemas.query import UploadQuery
from fastapi_app.containers import Container
from dependency_injector.wiring import inject, Provide

from .router import upload_router


@upload_router.post('/upload-entity')
@inject
async def upload_entity_endpoint(
        request: Request,
        files: list[UploadFile],
        params: UploadQuery = Query(),
        auth_depend=Depends(Provide[Container.auth_depend]),
        upload_handler = Depends(Provide[Container.upload_file_handler])
        ):
    user = await auth_depend.auth(request)
    await upload_handler.save_files_to_storage(user.storage_id, params.path_in_storage, files)
    return {"message": 'successfully uploaded files'}
