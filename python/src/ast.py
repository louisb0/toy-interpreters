from abc import ABC, abstractmethod

from src.token import Token


class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass


class Statement(Node, ABC):
    pass


class Expression(Node, ABC):
    pass


class Program(Node):
    def __init__(self):
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""


class LetStatement(Statement):
    def __init__(self, token: Token):
        self.token = token

        self.name: Identifier = None
        self.value: str = None

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"LetStatement: {self.name.value}"


class Identifier(Expression):
    def __init__(self, token: Token, literal: str):
        self.token = token
        self.value = literal

    def token_literal(self) -> str:
        return self.token.literal
