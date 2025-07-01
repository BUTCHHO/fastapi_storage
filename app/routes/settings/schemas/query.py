from pydantic import BaseModel


class AccountDeleteQuery(BaseModel):
    password: str