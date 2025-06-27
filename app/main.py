from fastapi import FastAPI
from .routes import download_router, auth_router, upload_router ,storage_acting_router ,view_storage_router

app = FastAPI()

app.include_router(view_storage_router)
app.include_router(storage_acting_router)
app.include_router(download_router)
app.include_router(upload_router)
app.include_router(auth_router)