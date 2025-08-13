from sqlalchemy.ext.asyncio import create_async_engine
from config import Config

async_engine = create_async_engine(Config.DATABASE_URL, pool_pre_ping=True)
