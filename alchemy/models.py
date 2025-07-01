from sqlalchemy import Column, Integer, String, Boolean, create_engine, Date, ForeignKey
from sqlalchemy.orm import declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)


Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255))
    name = Column(String(30), unique=True)
    is_admin = Column(Boolean, default=False)

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    expire_date = Column(Date)

Base.metadata.create_all(bind=engine)

