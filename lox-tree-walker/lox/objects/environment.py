from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from lox.lexer import Token

from lox.errors import RuntimeError


class Environment:
    def __init__(self, enclosing: "Environment | None" = None):
        self.enclosing = enclosing

        self.values = {}

    def define(self, name: str, value) -> None:
        self.values[name] = value

    def assign(self, token: "Token", value) -> None:
        if token.raw in self.values:
            self.values[token.raw] = value
            return

        if self.enclosing:
            self.enclosing.assign(token, value)
            return

        raise RuntimeError(token, f"Undefined variable '{token.raw}'.")

    def assign_at(self, distance: int, name: str, value):
        self._ancestor(distance).values[name] = value

    def get(self, token: "Token"):
        if token.raw in self.values:
            return self.values[token.raw]

        if self.enclosing:
            return self.enclosing.get(token)

        raise RuntimeError(token, f"Undefined variable '{token.raw}'.")

    def get_at(self, distance: int, name: str):
        return self._ancestor(distance).values[name]

    def _ancestor(self, distance: int) -> "Environment":
        ancestor = self

        for _ in range(distance):
            ancestor = cast(Environment, ancestor.enclosing)

        return ancestor
