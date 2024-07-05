from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lox.interpreter import Interpreter
    from lox.lexer import Token

from lox.objects.callables import Callable
from lox.errors import RuntimeError


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
        self.fields: dict[str, Any] = {}

    def get(self, name: "Token"):
        if name.raw in self.fields:
            return self.fields[name.raw]

        raise RuntimeError(name, f"Unknown property '{name.raw}'.")

    def set(self, name: "Token", value: Any):
        self.fields[name.raw] = value

    def __str__(self) -> str:
        return f"{self.klass} instance"
