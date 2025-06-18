from pydantic import BaseModel, Field


class DownloadQuery(BaseModel):
    entity_path_in_storage: str
