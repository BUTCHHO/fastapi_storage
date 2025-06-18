from pydantic import BaseModel, Field


class UploadQuery(BaseModel):
    path_in_storage: str

