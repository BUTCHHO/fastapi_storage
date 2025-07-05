from sqlalchemy.ext.asyncio import async_sessionmaker

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
                except Exception as e:
                    await session.rollback()
                    raise
        return wrapper
