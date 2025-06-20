from pydantic import BaseModel
from typing import List


class ViewStorageResponse(BaseModel):
    entities: list