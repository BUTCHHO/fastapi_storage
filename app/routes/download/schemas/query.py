from pydantic import BaseModel


class DownloadQuery(BaseModel):
    entity_path_in_storage: str
