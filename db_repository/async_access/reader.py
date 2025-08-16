from db_repository.async_access.async_parent_access import ParentAccess
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

class ModelReader(ParentAccess):
    def __init__(self, model, logger, engine):
        self.session = async_sessionmaker(engine, expire_on_commit=False)
        super().__init__(model, logger, engine)

    @ParentAccess.async_connection
    async def get_by_kwargs(self,session, **kwargs):
        statement = select(self.model).filter_by(**kwargs).limit(1)
        result = await session.execute(statement)
        return result.scalar_one_or_none()


    @ParentAccess.async_connection
    async def get_by_id(self, session, id):
        statement = select(self.model).filter_by(id=id).limit(1)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
