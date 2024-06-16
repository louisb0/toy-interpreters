from abc import ABC, abstractmethod

from lox.lexer import Token


class Expression(ABC):
    pass


class ExpressionVisitor(ABC):
    @abstractmethod
    def visitUnaryExpression(self, expr: "Unary"):
        pass

    @abstractmethod
    def visitLiteralExpression(self, expr: "Literal"):
        pass

    @abstractmethod
    def visitGroupingExpression(self, expr: "Grouping"):
        pass

    @abstractmethod
    def visitBinaryExpression(self, expr: "Binary"):
        pass


class Unary(Expression):
    def __init__(self, right: Expression, operator: Token):
        self.right = right
        self.operator = operator

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visitUnaryExpression(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visitLiteralExpression(self)


class Grouping(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visitGroupingExpression(self)


class Binary(Expression):
    def __init__(self, right: Expression, token: Token, left: Expression):
        self.right = right
        self.token = token
        self.left = left

    def accept(self, visitor: ExpressionVisitor):
        return visitor.visitBinaryExpression(self)
