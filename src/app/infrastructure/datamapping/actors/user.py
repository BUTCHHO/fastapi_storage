from csv import DictWriter



from app.application.common.ports.user_command_gateway import UserCommandGateway
from app.infrastructure.datamapping.models import user_fieldnames
from app.domain.entities.user import User


class UserActorCSV(UserCommandGateway):
    def __init__(self, csv_file_path):
        self._csv_file_path = csv_file_path

    def add(self, user: User) -> None:
        with open(self._csv_file_path) as file:
            writer = DictWriter(file, user_fieldnames)
            writer.writerow(user.__dict__)


