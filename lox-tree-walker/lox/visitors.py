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


class TreePrinter(Visitor):
    def print(self, expr: "ast.Expression") -> str:
        return expr.accept(self)

    def visitUnaryExpression(self, expr: "ast.Unary") -> str:
        return f"{expr.operator.raw}({expr.right.accept(self)})"

    def visitLiteralExpression(self, expr: "ast.Literal") -> str:
        return str(expr.value)

    def visitGroupingExpression(self, expr: "ast.Grouping") -> str:
        return f"(group: {expr.expr.accept(self)})"

    def visitBinaryExpression(self, expr: "ast.Binary") -> str:
        return (
            f"({expr.left.accept(self)} {expr.token.raw} ({expr.right.accept(self)}))"
        )
