from pydantic import BaseModel


class GetEntitiesResponse(BaseModel):
    path_in_storage: str | None
    entities: list[str] | list

class SearchEntitiesResponse(BaseModel):
    entities: list[str] | list