from pydantic import BaseModel, Field


class SignUpQuery(BaseModel):
    name: str = Field(max_length=16, min_length=1)
    password: str = Field(max_length=255)

class AuthenticateQuery(BaseModel):
    name: str
    password: str