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

    #TODO отправляет пустые файлы. Надо исправить



@app.post('/upload-entity')
async def upload_entity_endpoint(path: str, files: list[UploadFile]):
    abs_path = storage_reader.join_with_root_path(path)
    def is_path_valid(a): pass #TODO затычка
    if not is_path_valid(abs_path):
        return HTTPException(400, {'message': 'invalid path'})
    for file in files:
        fpath = f'{abs_path}/{file.filename}'
        await storage_writer.async_write_from_fastapi_uploadfile_to_file(file, fpath)




