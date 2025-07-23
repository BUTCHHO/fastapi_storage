from sqlalchemy.ext.asyncio import create_async_engine
from config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)