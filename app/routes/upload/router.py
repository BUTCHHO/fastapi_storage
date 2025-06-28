from fastapi import APIRouter, UploadFile, Query, Depends
from .schemas.query import UploadQuery
from .endpoint_handlers import UploadFileHandler
from app.singletones import storage_writer, path_ensurer, logger, path_joiner

from app.routes.dependencies import auth_depend

upload_router = APIRouter()

upload_handler = UploadFileHandler(storage_writer, path_ensurer, logger, path_joiner)

@upload_router.post('/upload-entity')
async def upload_entity_endpoint(files: list[UploadFile], params: UploadQuery = Query(), user=Depends(auth_depend.auth)):
    #TODO это дерьмо не работает
    # если пытатсься создать файл прямо в корне директории юзера, то пазлиб вместо ттго чтобы ОБЪЕДИНИТЬ ЭТИ ДВА ПУТИ возвращает имя файла как оно есть
    # Я ВООБЗЕ НЕ НЗАЮ ПОЧЕМУ ТАК Я НИКАК НЕ МЕНЯЛ ЛОГИКУ РАБОТЫ
    #


    await upload_handler.save_files_to_storage(str(user.id), params.path_in_storage, files)
    return {"message": 'successfully uploaded files'}
