from sqlalchemy import insert, delete

from db_repository.async_access.async_parent_access import ParentAccess


class ModelActor(ParentAccess):
    def __init__(self, model, logger, engine):
        super().__init__(model,logger,engine)

    def create_record(self, **kwargs):
        return self.model(**kwargs)

    @ParentAccess.async_connection
    async def create_and_write_record_to_db(self, session, **kwargs):
        record = self.create_record(**kwargs)
        session.add(record)
        await session.commit()

    @ParentAccess.async_connection
    async def delete_record_by_kwargs(self, session, **kwargs):
        statement = delete(self.model).filter_by(**kwargs)
        await session.execute(statement)
        await session.commit()