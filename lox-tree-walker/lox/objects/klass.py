from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lox.interpreter import Interpreter

from lox.objects.callables import Callable


class Class(Callable):
    def __init__(self, name: str):
        self.name = name

    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        return Instance(self)

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return self.name


class Instance:
    def __init__(self, klass: "Class"):
        self.klass = klass

    def __str__(self) -> str:
        return f"{self.klass} instance"
