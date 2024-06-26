from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast


class ExpressionVisitor(ABC):
    @abstractmethod
    def visitUnaryExpression(self, expr: "ast.expressions.Unary"):
        raise NotImplementedError()

    @abstractmethod
    def visitLiteralExpression(self, expr: "ast.expressions.Literal"):
        raise NotImplementedError()

    @abstractmethod
    def visitGroupingExpression(self, expr: "ast.expressions.Grouping"):
        raise NotImplementedError()

    @abstractmethod
    def visitBinaryExpression(self, expr: "ast.expressions.Binary"):
        raise NotImplementedError()

    @abstractmethod
    def visitVariableExpression(self, expr: "ast.expressions.Variable"):
        raise NotImplementedError()

    @abstractmethod
    def visitAssignmentExpression(self, expr: "ast.expressions.Assignment"):
        raise NotImplementedError()

    @abstractmethod
    def visitLogicalExpression(self, expr: "ast.expressions.Logical"):
        raise NotImplementedError()


class StatementVisitor(ABC):
    @abstractmethod
    def visitExpressionStatement(self, stmt: "ast.statements.Expression") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitPrintStatement(self, stmt: "ast.statements.Print") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitVarStatement(self, stmt: "ast.statements.Var") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitBlockStatement(self, stmt: "ast.statements.Block") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitIfStatement(self, stmt: "ast.statements.If") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitWhileStatement(self, stmt: "ast.statements.While") -> None:
        raise NotImplementedError()


class TreePrinter(ExpressionVisitor):
    def print(self, expr: "ast.expressions.Expression") -> str:
        return expr.accept(self)

    def visitUnaryExpression(self, expr: "ast.expressions.Unary") -> str:
        return f"{expr.operator.raw}({expr.right.accept(self)})"

    def visitLiteralExpression(self, expr: "ast.expressions.Literal") -> str:
        return str(expr.value)

    def visitGroupingExpression(self, expr: "ast.expressions.Grouping") -> str:
        return f"(group: {expr.expr.accept(self)})"

    def visitBinaryExpression(self, expr: "ast.expressions.Binary") -> str:
        return (
            f"({expr.left.accept(self)} {expr.token.raw} ({expr.right.accept(self)}))"
        )
