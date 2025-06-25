from sqlalchemy.orm import sessionmaker
from alchemy.models import engine

class ParentAccess:
    def __init__(self, model, logger):
        self.session = sessionmaker(engine)
        self.model = model
        self.logger = logger