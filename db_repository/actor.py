from .parent_access import ParentAccess

class ModelActor(ParentAccess):
    def __init__(self, model, logger):
        super().__init__(model, logger)

    def create_and_write_record_to_db(self, **kwargs):
        record = self.create_record(**kwargs)
        self.write_record_to_db(record)

    def write_record_to_db(self, record):
        session = self.session()
        try:
            session.add(record)
            session.commit()
        finally:
            session.close()

    def create_record(self, **kwargs):
        try:
            return self.model(**kwargs)
        except Exception as e:
            self.logger.log(e)

    def delete_record_by_id(self, id):
        session = self.session()
        try:
            session.query(self.model).filter_by(id=id).delete()
            session.commit()
        except Exception as e:
            self.logger.log(e)
            session.rollback()
        finally:
            session.close()

    def delete_record_by_kwargs(self, **kwargs):
        session = self.session()
        try:
            session.query(self.model).filter_by(**kwargs).delete()
            session.commit()
        except Exception as e:
            self.logger.log(e)
            session.rollback()
        finally:
            session.close()