from .engine import engine

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base(engine)


class User(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))
    name = Column(String(30), unique=True)
    is_admin = Column(Boolean, default=False)
    owning_dir_id = Column(Integer, unique=True)


