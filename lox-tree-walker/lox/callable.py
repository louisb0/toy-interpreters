from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.interpreter import Interpreter


class Callable(ABC):
    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list):
        pass

    @abstractmethod
    def arity(self) -> int:
        pass
