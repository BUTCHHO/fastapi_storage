from pydantic import BaseModel, Field


class UploadQuery(BaseModel):
    user_id: int = Field(ge=0)
    path_in_storage: str

