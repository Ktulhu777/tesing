from pydantic import BaseModel


class MemesGetAll(BaseModel):
    object_name: str
    url: str
