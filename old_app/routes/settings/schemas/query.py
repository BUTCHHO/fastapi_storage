from pydantic import BaseModel


class AccountDeleteQuery(BaseModel):
    password: str
    should_delete_storage: bool = False