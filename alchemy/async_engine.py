from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine('postgresql+asyncpg://butcho:56745321@localhost:5432/cloud_storage', pool_pre_ping=True)