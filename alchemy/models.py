from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))
    name = Column(String(30), unique=True)
    is_admin = Column(Boolean, default=False)
    owning_dir_id = Column(Integer, unique=True)

Base.metadata.create_all(bind=engine)

