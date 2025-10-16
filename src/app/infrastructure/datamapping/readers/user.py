from csv import DictReader
from json import loads

from typing import List

from app.application.common.ports.user_query_gateway import UserQueryGateway
from app.domain.entities.user import User


class UserReaderCSV(UserQueryGateway):
    def __init__(self, csv_file_path):
        self._csv_file = csv_file_path

    async def read_all(self, limit:int, offset:int) -> List[User]:
        with open(self._csv_file) as csv_file:
            csv_reader = DictReader(csv_file)
            list_of_users = [User(id_=row['id'],
                                  user_name=row['user_name'],
                                  password_hash=row['password_hash'],
                                  user_role=row['role'],
                                  is_active=row['is_active'],
                                  repositories_roles=loads(row['repositories_roles']))
                             for row in csv_reader][offset:limit]
            return list_of_users