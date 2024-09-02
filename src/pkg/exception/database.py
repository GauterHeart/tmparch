from .base import BaseExceptionHandler


class NotFoundException(BaseExceptionHandler):
    status_code = 404
    detail = "Not found element in db"


class InsertException(BaseExceptionHandler):
    status_code = 404
    detail = "Cant insert row"


class UpdateException(BaseExceptionHandler):
    status_code = 404
    detail = "Cant update row"


class ValueAlreadyExistException(BaseExceptionHandler):
    status_code = 400
    detail = "value already exists"


class MapIsNotSerializedException(BaseExceptionHandler):
    status_code = 500
    detail = "Map is not Serialized"
