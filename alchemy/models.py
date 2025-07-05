from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from asyncio import run
from .async_engine import async_engine

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))
    name = Column(String(30), unique=True)
    is_admin = Column(Boolean, default=False)
    storage_id = Column(String(32), unique = True)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    expire_date = Column(Date)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

run(create_tables())