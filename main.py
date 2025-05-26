from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from os import getenv

load_dotenv('/home/butcho/пайтон проекты/media_storage/.env')
STORAGE_PATH = getenv('STORAGE_PATH')
from logic import StorageReader, StorageWriter, Archivator
from utils import validate_path, log
from exceptions import PathGoesBeyondLimits
from path_explorator.exceptions import EntityDoesNotExists, EntityIsNotADir
from path_explorator import PathCreator
from urllib.parse import quote



app = FastAPI()
storage_reader = StorageReader()
storage_writer = StorageWriter()
archivator = Archivator()
path_creator = PathCreator()

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
    if not storage_reader.is_exists(entity_path_in_storage):
        return HTTPException(status_code=404, detail={"message": f'entity at {entity_path_in_storage} does not exists', "code": 'entity_does_not_exists'})

    if storage_reader.is_dir(entity_path_in_storage):
        zip_path = archivator.create_large_zip(entity_path_in_storage)
        background_tasks.add_task(archivator.cleanup_temp_files, zip_path)

        return FileResponse(
            zip_path,
            filename=f"{zip_path.name}",
            media_type="application/zip"
        )
    elif storage_reader.is_file(entity_path_in_storage):
        entity_name = storage_reader.get_name(entity_path_in_storage)
        encoded_entity_name = quote(entity_name)
        entity_abs_path = storage_reader.join_with_root_path(entity_path_in_storage)
        return FileResponse(
            entity_abs_path,
            filename=entity_name,
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_entity_name}"}
        )

@app.post('/upload-entity')
async def upload_entity_endpoint(path: str, files: list[UploadFile]):
    abs_path = f'{STORAGE_PATH}/{path}'
    try:
        validate_path(abs_path)
        for file in files:
            fpath = f'{abs_path}/{file.filename}'
            await storage_writer.async_write_from_fastapi_uploadfile_to_file(file, fpath)
    except PathGoesBeyondLimits as e:
        log(e)
        return HTTPException(403, {"message": 'path goes beyond permitted limits', "code": 'path_goes_beyond_permitted_limits'})
