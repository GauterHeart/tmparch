class RabbitInvalidHandlerFunctionException(Exception):
    def __init__(self) -> None:
        self.msg = "Rabbit invalid handler function"

    def __str__(self) -> str:
        return "{}".format(self.msg)


class RabbitInvalidModelTypeException(Exception):
    def __init__(self) -> None:
        self.msg = "Rabbit invalid model type"

    def __str__(self) -> str:
        return "{}".format(self.msg)
