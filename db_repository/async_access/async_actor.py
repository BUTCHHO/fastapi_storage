from sqlalchemy import insert, delete, update
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from db_repository.async_access.async_parent_access import ParentAccess
from exceptions.database_repo import FieldUniqueViolation


class ModelActor(ParentAccess):
    def __init__(self, model, engine):
        super().__init__(model,engine)

    def create_record(self, **kwargs):
        return self.model(**kwargs)

    @ParentAccess.async_connection
    async def create_and_write_record_to_db(self, session, **kwargs):
        record = self.create_record(**kwargs)
        session.add(record)
        await session.commit()

    @ParentAccess.async_connection
    async def write_record_to_db(self, session, record):
        session.add(record)
        await session.commit()

    @ParentAccess.async_connection
    async def delete_record_by_kwargs(self, session, **kwargs):
        statement = delete(self.model).filter_by(**kwargs)
        await session.execute(statement)
        await session.commit()

    @ParentAccess.async_connection
    async def delete_record_by_id(self, session, id):
        statement = delete(self.model).filter_by(id=id)
        await session.execute(statement)
        await session.commit()

    @ParentAccess.async_connection
    async def change_values_by_kwargs(self, session, new_values:dict, **kwargs):
        statement = update(self.model).filter_by(**kwargs).values(**new_values)
        await session.execute(statement)
        await session.commit()
