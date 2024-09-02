from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class HttpResponseSchema(BaseModel, Generic[T]):
    payload: T
