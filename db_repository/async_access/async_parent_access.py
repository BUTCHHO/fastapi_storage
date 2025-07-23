from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import IntegrityError
from asyncpg import UniqueViolationError
from exceptions.database_repo import FieldUniqueViolation

class ParentAccess:
    def __init__(self, model, logger, engine):
        self.model = model
        self.logger = logger
        self.engine = engine
        self.async_session_maker = async_sessionmaker(engine)

    @staticmethod
    def async_connection(method):
        async def wrapper(self, *args, **kwargs):
            async with self.async_session_maker() as session:
                try:
                    return await method(self, session=session, **kwargs)
                except IntegrityError as i_e:
                    if 'UniqueViolationError' in i_e.orig.__str__():
                        raise FieldUniqueViolation()
                    raise
                except Exception as e:
                    await session.rollback()
                    raise
        return wrapper
