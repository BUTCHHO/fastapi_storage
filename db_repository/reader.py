from sqlalchemy.orm import sessionmaker, Session
from alchemy.models import engine
from interfaces import ILogger


class ModelAccess:
    def __init__(self, model, logger):
        self.session = sessionmaker(engine)
        self.model = model
        self.logger: ILogger = logger



    def get_by_id(self, id):
        session: Session = self.session()
        try:
            return session.query(self.model).filter_by(id=id).first()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()

    def get_by_kwargs(self, **kwargs):
        session: Session = self.session()
        try:
             return session.query(self.model).filter_by(**kwargs).first()
        except Exception as e:
            self.logger.log(e)
        finally:
            session.close()

    def create_record(self, **kwargs):
        session: Session = self.session()
        try:
            record = self.model(**kwargs)
            session.add(record)
            session.commit()
        except Exception as e:
            self.logger.log(e)
            session.rollback()
        finally:
            session.close()

    def delete_record_by_id(self, id):
        session: Session = self.session()
        try:
            session.query(self.model).filter_by(id=id).delete()
            session.commit()
        except:
            self.logger.log(e)
            session.rollback()
        finally:
            session.close()

    def delete_record_by(self, **kwargs):
        session: Session = self.session()
        try:
            session.query(self.model).filter_by(**kwargs).delete()
            session.commit()
        except:
            self.logger.log(e)
            session.rollback()
        finally:
            session.close()