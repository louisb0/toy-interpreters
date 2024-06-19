from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token
    from lox.visitors import Visitor


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: "Visitor"):
        raise NotImplementedError()


class Unary(Expression):
    def __init__(self, operator: "Token", right: Expression):
        self.operator = operator
        self.right = right

    def accept(self, visitor: "Visitor"):
        return visitor.visitUnaryExpression(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: "Visitor"):
        return visitor.visitLiteralExpression(self)


class Grouping(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr

    def accept(self, visitor: "Visitor"):
        return visitor.visitGroupingExpression(self)


class Binary(Expression):
    def __init__(self, left: Expression, token: "Token", right: Expression):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor: "Visitor"):
        return visitor.visitBinaryExpression(self)
