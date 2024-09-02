from typing import List

from src.model.admin import AdminModel
from src.pkg.arch.response import HttpResponseSchema


class FetchAdminResponseSchema(HttpResponseSchema):
    payload: List[AdminModel]
