from pydantic import BaseModel


class GetEntitiesResponse(BaseModel):
    entities: list[str] | list

class SearchEntitiesResponse(BaseModel):
    entities: list[str] | list