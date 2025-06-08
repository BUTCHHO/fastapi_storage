from pydantic import BaseModel, Field

class ViewStorageRootQuery(BaseModel):
    user_id: int = Field(ge=0)

class ViewStorageQuery(BaseModel):
    user_id: int = Field(ge=0)
    entity_path_in_storage: str
