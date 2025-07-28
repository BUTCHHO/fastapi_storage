from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import config
from .routes import download_router, settings_router, auth_router, upload_router ,storage_acting_router ,browser_router
from alchemy.models import Base
from alchemy.async_engine import init_async_engine, get_async_engine


class ApplicationManager:
    def __init__(self):

        self.config = {'DATABASE_URL': config.DATABASE_URL,
                       'CACHE_PORT':config.CACHE_PORT,
                       'CACHE_HOST': config.CACHE_HOST}
        init_async_engine(self.config['DATABASE_URL'])
        self.database_engine = get_async_engine()
        self.redis_client =
        self.app = FastAPI(lifespan=self.lifespan)

        self.browser_static_dir = Path(__file__).parent / 'routes/browser/static'
        self.global_static_dir = Path(__file__).parent / 'static'

        self.browser_static = StaticFiles(directory=self.browser_static_dir)
        self.global_static = StaticFiles(directory=self.global_static_dir)

        self.app.mount('/browser/static', self.browser_static, 'browser_static')
        self.app.mount('/static', self.global_static, 'static')

        self.app.include_router(browser_router)
        self.app.include_router(storage_acting_router)
        self.app.include_router(download_router)
        self.app.include_router(upload_router)
        self.app.include_router(auth_router)
        self.app.include_router(settings_router)



    @asynccontextmanager
    async def lifespan(self, application: FastAPI):
        async with self.database_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield

    def get_app(self):
        return self.app

    def configure_app_for_tests(self, test_database_url, test_cache_url):
        init_async_engine(test_database_url)
        self.database_engine = get_async_engine()



app_manager = ApplicationManager()
app = app_manager.get_app()

