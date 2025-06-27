from pydantic import BaseModel, Field


class MakeDirInStorageQuery(BaseModel):
    path_in_storage: str | None = None
    name: str = Field(max_length=255, min_length=1)