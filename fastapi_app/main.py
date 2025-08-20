from fastapi import FastAPI


from contextlib import asynccontextmanager

from .routes import download_router, settings_router, auth_router, upload_router ,storage_acting_router ,browser_router
from .middlewares.exception_middleware import ExceptionCatcherMiddleware
from alchemy.models import Base
from alchemy.async_engine import async_engine

from config import Config

from .containers import Container


container = Container()


container.wire(['app.routes.authorization.endpoints', 'app.routes.browser.endpoints', 'app.routes.download.endpoints',
                'app.routes.settings.endpoints', 'app.routes.storage_acting.endpoints', 'app.routes.upload.endpoints'])

container.config.from_dict(Config.to_dict())

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(ExceptionCatcherMiddleware)


app.include_router(browser_router)
app.include_router(storage_acting_router)
app.include_router(download_router)
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(settings_router)