from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lox.interpreter import Interpreter
    from lox.lexer import Token

from lox.objects.callables import Callable, Function
from lox.errors import RuntimeError


class Class(Callable):
    def __init__(self, name: str, methods: dict[str, "Function"]):
        self.name = name
        self.methods = methods

    def find_method(self, name: str) -> "Function | None":
        return self.methods.get(name)

    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        instance = Instance(self)

        initialiser = self.find_method("init")
        if initialiser:
            initialiser.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initialiser = self.find_method("init")
        return initialiser.arity() if initialiser else 0

    def __str__(self) -> str:
        return self.name


class Instance:
    def __init__(self, klass: "Class"):
        self.klass = klass
        self.fields: dict[str, Any] = {}

    def get(self, name: "Token"):
        if name.raw in self.fields:
            return self.fields[name.raw]

        method = self.klass.find_method(name.raw)
        if method:
            return method.bind(self)

        raise RuntimeError(name, f"Unknown property '{name.raw}'.")

    def set(self, name: "Token", value: Any):
        self.fields[name.raw] = value

    def __str__(self) -> str:
        return f"{self.klass} instance"
