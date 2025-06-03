from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from os import getenv

load_dotenv('/home/butcho/пайтон проекты/media_storage/.env')
STORAGE_PATH = getenv('STORAGE_PATH')

from logic import StorageReader, StorageWriter, Archivator
from utils import PathValidEnsurer, Logger
from view_handlers import FileResponseHandler, UploadFileHandler
from path_explorator import EntityDoesNotExists, EntityIsNotADir
from path_explorator import PathCreator



app = FastAPI()
logger = Logger()
path_ensurer = PathValidEnsurer(STORAGE_PATH)
storage_reader = StorageReader(STORAGE_PATH)
storage_writer = StorageWriter(STORAGE_PATH)
archivator = Archivator()
path_creator = PathCreator()
file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer)
upload_handler = UploadFileHandler(storage_reader,storage_writer, path_ensurer, logger)



@app.get('/storage/{user_id}')
def view_storage_root(user_id: int):
    try:
        entities = storage_reader.get_all_entitynames_in_dir(str(user_id))
        return entities
    except Exception as e:
        logger.log(e)
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
   await upload_handler.save_files_to_storage(path, files)




