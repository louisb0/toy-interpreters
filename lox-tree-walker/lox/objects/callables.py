from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.interpreter import Interpreter

from lox.objects import Environment


class Return(Exception):
    def __init__(self, value):
        super().__init__()

        self.value = value


class Callable(ABC):
    @abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list) -> Any:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass


class Function(Callable):
    def __init__(self, declaration: "ast.statements.Function", closure: "Environment"):
        self.closure = closure
        self.declaration = declaration

    def call(self, interpreter: "Interpreter", arguments: list):
        env = Environment(self.closure)
        for i, param in enumerate(self.declaration.params):
            env.define(param.raw, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, env)
        except Return as e:
            return e.value

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.raw}>"


class NativeClock(Callable):
    def call(self, interpreter: "Interpreter", arguments: list):
        import time

        return time.time()

    def arity(self) -> int:
        return 0
