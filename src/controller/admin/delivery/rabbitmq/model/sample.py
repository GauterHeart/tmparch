from pydantic import BaseModel


class SampleAdminModel(BaseModel):
    name: str
