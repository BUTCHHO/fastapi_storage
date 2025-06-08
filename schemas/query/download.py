from pydantic import BaseModel, Field


class DownloadQuery(BaseModel):
    user_id: int = Field(ge=0)
    entity_path_in_storage: str
