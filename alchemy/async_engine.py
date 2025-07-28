from sqlalchemy.ext.asyncio import create_async_engine
from config import DATABASE_URL

async_engine = None

def init_async_engine(db_url):
    global async_engine
    if async_engine:
        async_engine.dispose()
    async_engine = create_async_engine(db_url)

def get_async_engine():
    global async_engine
    if async_engine is None:
        raise RuntimeError('async_engine is not initialized')
    return async_engine