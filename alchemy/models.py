from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base

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