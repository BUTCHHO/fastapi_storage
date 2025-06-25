from pydantic import BaseModel, Field


class UploadQuery(BaseModel):
    path_in_storage: str | None = None

class MakeDirInStorageQuery(BaseModel):
    path_in_storage: str | None = None
    name: str

