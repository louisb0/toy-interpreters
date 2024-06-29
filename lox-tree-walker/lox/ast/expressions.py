from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token
    from lox.visitors import ExpressionVisitor


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor: "ExpressionVisitor"):
        raise NotImplementedError()


class Unary(Expression):
    def __init__(self, operator: "Token", right: "Expression"):
        self.operator = operator
        self.right = right

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitUnaryExpression(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitLiteralExpression(self)


class Grouping(Expression):
    def __init__(self, expr: "Expression"):
        self.expr = expr

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitGroupingExpression(self)


class Binary(Expression):
    def __init__(self, left: "Expression", token: "Token", right: "Expression"):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitBinaryExpression(self)


class Variable(Expression):
    def __init__(self, name: "Token"):
        self.name = name

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitVariableExpression(self)


class Assignment(Expression):
    def __init__(self, name: "Token", value: "Expression"):
        self.name = name
        self.value = value

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitAssignmentExpression(self)


class Logical(Expression):
    def __init__(self, left: "Expression", token: "Token", right: "Expression"):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitLogicalExpression(self)


class Call(Expression):
    def __init__(
        self, callee: "Expression", paren: "Token", arguments: list["Expression"]
    ):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visitCallExpression(self)
