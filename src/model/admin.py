from datetime import datetime

from pydantic import BaseModel, Field


class _AdminModel(BaseModel): ...


class AdminFieldMap(_AdminModel):
    class Id(_AdminModel):
        id: int = Field(
            description="ID",
        )

    class Name(_AdminModel):
        name: str = Field(
            description="unique name",
        )

    class DateCreate(_AdminModel):
        date_create: datetime = Field(
            description="Created at",
        )

    class DateUpdate(_AdminModel):
        date_update: datetime = Field(
            description="Created at",
        )


class AdminModel(
    AdminFieldMap.Id,
    AdminFieldMap.Name,
    AdminFieldMap.DateCreate,
    AdminFieldMap.DateUpdate,
): ...
