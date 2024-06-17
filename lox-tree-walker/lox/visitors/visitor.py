from abc import ABC, abstractmethod

import lox.ast as ast


class Visitor(ABC):
    @abstractmethod
    def visitUnaryExpression(self, expr: ast.Unary):
        pass

    @abstractmethod
    def visitLiteralExpression(self, expr: ast.Literal):
        pass

    @abstractmethod
    def visitGroupingExpression(self, expr: ast.Grouping):
        pass

    @abstractmethod
    def visitBinaryExpression(self, expr: ast.Binary):
        pass