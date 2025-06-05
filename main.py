from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from os import getenv

load_dotenv('/home/butcho/пайтон проекты/media_storage/.env')
STORAGE_PATH = getenv('STORAGE_PATH')

from logic import StorageReader, StorageWriter, Archivator
from utils import PathValidEnsurer, Logger
from view_handlers import FileResponseHandler, UploadFileHandler, StorageViewHandler
from path_explorator import EntityDoesNotExists, EntityIsNotADir
from path_explorator import PathCreator


#TODO добавить HTTPException code 500 после логирования неизвестных ошибок
# можно попробовать перехватывать ошибки следующим образом
# raise_if_path_invalid()
# если метод поднимает ошибку, которая нас неинтересует (например, мы допускаем EntityDoesNotExists
# можно отловить лишь интересующие ошибки
# и в конце прописать except: pass
# это не вызовет лишний подъём исключения, но и не вынудит отлавливать каждое исклюение




app = FastAPI()
logger = Logger()
path_ensurer = PathValidEnsurer(STORAGE_PATH)
storage_reader = StorageReader(STORAGE_PATH)
storage_writer = StorageWriter(STORAGE_PATH)
archivator = Archivator()
path_creator = PathCreator()
file_response_handler = FileResponseHandler(archivator, storage_reader, logger, path_ensurer)
upload_handler = UploadFileHandler(storage_writer, path_ensurer, logger)
storage_view_handler = StorageViewHandler(storage_reader, logger, path_creator)

@app.get('/storage/{user_id}')
def view_storage_root(user_id: str):
    abs_path = storage_reader.join_with_root_path(user_id)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, user_id)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return entities


@app.get('/storage/{user_id}/{dpath:path}')
async def view_storage(user_id: str, dpath: str):
    path_in_storage = path_creator.join_paths(user_id, dpath)
    abs_path = storage_reader.join_with_root_path(path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, path_in_storage)
    entities = storage_view_handler.get_list_of_entities(abs_path)
    return entities

@app.get('/download-entity')
def download_entity_endpoint(entity_path_in_storage: str, background_tasks: BackgroundTasks):
    abs_path = storage_reader.join_with_root_path(entity_path_in_storage)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, entity_path_in_storage)
    response = file_response_handler.get_response(entity_path_in_storage)
    background_tasks.add_task(archivator.cleanup_temp_files)
    return response


@app.post('/upload-entity')
async def upload_entity_endpoint(path: str, files: list[UploadFile]):
    abs_path = storage_reader.join_with_root_path(path)
    path_ensurer.ensure_path_safety_on_endpoint_level(abs_path, path)
    await upload_handler.save_files_to_storage(abs_path, files)




