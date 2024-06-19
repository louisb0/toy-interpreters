from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast


class Visitor(ABC):
    @abstractmethod
    def visitUnaryExpression(self, expr: "ast.Unary"):
        raise NotImplementedError()

    @abstractmethod
    def visitLiteralExpression(self, expr: "ast.Literal"):
        raise NotImplementedError()

    @abstractmethod
    def visitGroupingExpression(self, expr: "ast.Grouping"):
        raise NotImplementedError()

    @abstractmethod
    def visitBinaryExpression(self, expr: "ast.Binary"):
        raise NotImplementedError()
