from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from os import getenv
load_dotenv('/home/butcho/пайтон проекты/media_storage/.env')
STORAGE_PATH = getenv('STORAGE_PATH')
from logic import StorageReader, StorageWriter, Archivator
from utils import raise_if_path_invalid, log
from view_handlers import FileResposeHandler
from path_explorator import EntityDoesNotExists, EntityIsNotADir, PathGoesBeyondLimits
from path_explorator import PathCreator



app = FastAPI()
storage_reader = StorageReader()
storage_writer = StorageWriter()
archivator = Archivator()
path_creator = PathCreator()
file_response_handler = FileResposeHandler(archivator,storage_reader)

@app.get('/storage/{user_id}')
def view_storage_root(user_id: int):
    try:
        entities = storage_reader.get_all_entitynames_in_dir(str(user_id))
        return entities
    except Exception as e:
        log(e)
        return e

@app.get('/storage/{user_id}/{dpath:path}')
async def view_storage(user_id: int, dpath: str):
    if '..' in dpath or dpath.startswith('/'):
        raise HTTPException(400, {
            "message": "Path cannot contain '..' or start with '/'",
            "code": "invalid_path"
        })
    path_to_dir = f'{user_id}/{dpath}'
    try:
        entities = storage_reader.get_all_entitynames_in_dir(path_to_dir)
    except EntityIsNotADir:
        raise HTTPException(
            400,
            {"message": f"Entity at {dpath} is not a directore", "code": 'not_a_dir'}
        )
    except EntityDoesNotExists:
        raise HTTPException(
            404,
            {"message": f"Entity at {dpath} does not exists", "code": "entity_does_not_exist"})
    return entities

@app.get('/download-entity')
def download_entity_endpoint(entity_path_in_storage: str, background_tasks: BackgroundTasks):
    response = file_response_handler.get_response(entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response



@app.post('/upload-entity')
async def upload_entity_endpoint(path: str, files: list[UploadFile]):
    abs_path = storage_reader.join_with_root_path(path)
    def is_path_valid(a): pass #TODO затычка
    if not is_path_valid(abs_path):
        return HTTPException(400, {'message': 'invalid path'})
    for file in files:
        fpath = f'{abs_path}/{file.filename}'
        await storage_writer.async_write_from_fastapi_uploadfile_to_file(file, fpath)


class LoadEntityEndpoints:
    def __init__(self): pass

    @staticmethod
    @app.get('/download-entity')
    def download_entity_endpoint(entity_path_in_storage: str, background_tasks: BackgroundTasks):
        absolute_entity_path = storage_reader.join_with_root_path(entity_path_in_storage)
        try:
            raise_if_path_invalid(absolute_entity_path)
        except PathGoesBeyondLimits:
            raise HTTPException(status_code=403, detail={"message": f'path {entity_path_in_storage} goes beyond limits', "code": 'path_goes_beyond_limits'})
        except EntityDoesNotExists:
            raise HTTPException(status_code=404, detail={"message": f'entity at {entity_path_in_storage} does not exists', "code": 'entity_does_not_exists'})


        if storage_reader.is_dir(entity_path_in_storage):
            zip_path = archivator.create_large_zip(absolute_entity_path)
            background_tasks.add_task(archivator.cleanup_temp_files, zip_path)

            return FileResponse(
                zip_path,
                filename=f"{zip_path.name}",
                media_type="application/zip"
            )
        elif storage_reader.is_file(entity_path_in_storage):
            entity_name = storage_reader.get_name(entity_path_in_storage)
            encoded_entity_name = quote(entity_name)
            return FileResponse(
                absolute_entity_path,
                filename=entity_name,
                headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"},
                content_disposition_type="attachment"
            )

    @staticmethod
    @app.post('/upload-entity')
    async def upload_entity_endpoint(path: str, files: list[UploadFile]):
        abs_path = storage_reader.join_with_root_path(path)

        def is_path_valid(a):
            pass  # TODO затычка

        if not is_path_valid(abs_path):
            return HTTPException(400, {'message': 'invalid path'})
        for file in files:
            fpath = f'{abs_path}/{file.filename}'
            await storage_writer.async_write_from_fastapi_uploadfile_to_file(file, fpath)


