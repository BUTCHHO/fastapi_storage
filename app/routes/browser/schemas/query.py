from pydantic import BaseModel


class ViewStorageQuery(BaseModel):
    path_in_storage: str | None = None