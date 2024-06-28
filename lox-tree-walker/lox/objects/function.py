from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.interpreter import Interpreter

from lox.objects import Callable, Environment


class Function(Callable):
    def __init__(self, declaration: "ast.statements.Function"):
        self.declaration = declaration

    def call(self, interpreter: "Interpreter", arguments: list):
        env = Environment(interpreter.globals)
        for i, param in enumerate(self.declaration.params):
            env.define(param.raw, arguments[i])

        interpreter.execute_block(self.declaration.body, env)

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.raw}>"
