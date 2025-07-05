from sqlalchemy.orm import sessionmaker

class ParentAccess:
    def __init__(self, model, logger, engine):
        self.session = sessionmaker(engine)
        self.model = model
        self.logger = logger