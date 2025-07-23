from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routes import download_router, settings_router, auth_router, upload_router ,storage_acting_router ,browser_router
from alchemy.models import Base
from alchemy.async_engine import async_engine

browser_static_dir = Path(__file__).parent / 'routes/browser/static'
global_static_dir = Path(__file__).parent / 'static'

browser_static = StaticFiles(directory=browser_static_dir)
global_static = StaticFiles(directory=global_static_dir)


app = FastAPI()


@app.on_event('startup')
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.mount('/browser/static', browser_static, 'browser_static')
app.mount('/static', global_static, 'static')

app.include_router(browser_router)
app.include_router(storage_acting_router)
app.include_router(download_router)
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(settings_router)