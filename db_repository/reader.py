from sqlalchemy.orm import Session

from .parent_access import ParentAccess

class ModelReader(ParentAccess):
    def __init__(self, model, logger):
        super().__init__(model, logger)

    def get_by_id(self, id):
        session = self.session()
        try:
            return session.query(self.model).filter_by(id=id).first()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()

    def get_by_kwargs(self, **kwargs):
        session = self.session()
        try:
             return session.query(self.model).filter_by(**kwargs).first()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()

    def does_record_with_id_exists(self, id):
        session: Session = self.session()
        try:
            return session.query(self.model).filter_by(id=id).exists()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()

    def does_record_with_kwargs_exists(self, **kwargs):
        session = self.session()
        try:
            return session.query(self.model).filter_by(**kwargs).exists()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()