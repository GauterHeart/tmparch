from src.pkg.exception import BaseExceptionHandler


class RabbitModelValidatorException(BaseExceptionHandler):
    status_code = 422
    detail = "Model is not valid"
