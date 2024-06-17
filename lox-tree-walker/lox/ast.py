from abc import ABC

from lox.lexer import Token
from lox.visitors import Visitor


class Expression(ABC):
    pass


class Unary(Expression):
    def __init__(self, right: Expression, operator: Token):
        self.right = right
        self.operator = operator
        
    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpression(self)
    

class Literal(Expression):
    def __init__(self, value):
        self.value = value
        
    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpression(self)
    

class Grouping(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr
        
    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpression(self)
    

class Binary(Expression):
    def __init__(self, right: Expression, token: Token, left: Expression):
        self.right = right
        self.token = token
        self.left = left
        
    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpression(self)