from pydantic import BaseModel, Field


class BrowserGetEntitiesQuery(BaseModel):
    path_in_storage: str | None = None

class BrowserSearchEntitiesQuery(BaseModel):
    searching_in_path: str | None = None
    pattern: str