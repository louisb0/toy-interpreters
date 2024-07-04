from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast


class ExpressionVisitor(ABC):
    @abstractmethod
    def visit_unary_expression(self, expr: "ast.expressions.Unary"):
        raise NotImplementedError()

    @abstractmethod
    def visit_literal_expression(self, expr: "ast.expressions.Literal"):
        raise NotImplementedError()

    @abstractmethod
    def visit_grouping_expression(self, expr: "ast.expressions.Grouping"):
        raise NotImplementedError()

    @abstractmethod
    def visit_binary_expression(self, expr: "ast.expressions.Binary"):
        raise NotImplementedError()

    @abstractmethod
    def visit_variable_expression(self, expr: "ast.expressions.Variable"):
        raise NotImplementedError()

    @abstractmethod
    def visit_assignment_expression(self, expr: "ast.expressions.Assignment"):
        raise NotImplementedError()

    @abstractmethod
    def visit_logical_expression(self, expr: "ast.expressions.Logical"):
        raise NotImplementedError()

    @abstractmethod
    def visit_call_expression(self, expr: "ast.expressions.Call"):
        raise NotImplementedError()


class StatementVisitor(ABC):
    @abstractmethod
    def visit_expression_statement(self, stmt: "ast.statements.Expression") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_print_statement(self, stmt: "ast.statements.Print") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_var_statement(self, stmt: "ast.statements.Var") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_block_statement(self, stmt: "ast.statements.Block") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_if_statement(self, stmt: "ast.statements.If") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_while_statement(self, stmt: "ast.statements.While") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_function_statement(self, stmt: "ast.statements.Function") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_return_statement(self, stmt: "ast.statements.Return") -> None:
        raise NotImplementedError()

    @abstractmethod
    def visit_class_statement(self, stmt: "ast.statements.Class") -> None:
        raise NotImplementedError()


class TreePrinter(ExpressionVisitor):
    def print(self, expr: "ast.expressions.Expression") -> str:
        return expr.accept(self)

    def visit_unary_expression(self, expr: "ast.expressions.Unary") -> str:
        return f"{expr.operator.raw}({expr.right.accept(self)})"

    def visit_literal_expression(self, expr: "ast.expressions.Literal") -> str:
        return str(expr.value)

    def visit_grouping_expression(self, expr: "ast.expressions.Grouping") -> str:
        return f"(group: {expr.expr.accept(self)})"

    def visit_binary_expression(self, expr: "ast.expressions.Binary") -> str:
        return (
            f"({expr.left.accept(self)} {expr.token.raw} ({expr.right.accept(self)}))"
        )
