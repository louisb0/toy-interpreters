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
        return visitor.visit_unary_expression(self)


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_literal_expression(self)


class Grouping(Expression):
    def __init__(self, expr: "Expression"):
        self.expr = expr

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_grouping_expression(self)


class Binary(Expression):
    def __init__(self, left: "Expression", token: "Token", right: "Expression"):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_binary_expression(self)


class Variable(Expression):
    def __init__(self, name: "Token"):
        self.name = name

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_variable_expression(self)


class Assignment(Expression):
    def __init__(self, name: "Token", value: "Expression"):
        self.name = name
        self.value = value

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_assignment_expression(self)


class Logical(Expression):
    def __init__(self, left: "Expression", token: "Token", right: "Expression"):
        self.left = left
        self.token = token
        self.right = right

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_logical_expression(self)


class Call(Expression):
    def __init__(
        self, callee: "Expression", paren: "Token", arguments: list["Expression"]
    ):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_call_expression(self)


class Get(Expression):
    def __init__(self, object: "Expression", name: "Token"):
        self.object = object
        self.name = name

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_get_expression(self)


class Set(Expression):
    def __init__(self, object: "Expression", name: "Token", value: "Expression"):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_set_expression(self)


class This(Expression):
    def __init__(self, keyword: "Token"):
        self.keyword = keyword

    def accept(self, visitor: "ExpressionVisitor"):
        return visitor.visit_this_expression(self)
