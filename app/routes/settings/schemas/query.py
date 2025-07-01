from pydantic import BaseModel


class AccountDeleteQuery(BaseModel):
    name: str
    password: str