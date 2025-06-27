from pydantic import BaseModel


class ViewStorageResponse(BaseModel):
    entities: list