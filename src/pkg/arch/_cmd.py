from abc import ABC, abstractmethod
from typing import Dict, Type

__all__ = ["CMD", "Init"]


class CMD(ABC):
    name: str = NotImplemented

    @abstractmethod
    def run(self) -> None: ...


class Init:
    APP_MAP: Dict[str, Type[CMD]] = NotImplemented
