from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.lexer import Token

from lox.visitors import ExpressionVisitor, StatementVisitor
from lox.lexer import TokenType


class RuntimeError(Exception):
    def __init__(self, token: "Token", message: str):
        super().__init__(message)

        self.token = token


class Interpreter(ExpressionVisitor, StatementVisitor):
    def interpret(self, statements: list["ast.statements.Statement"]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            from lox import Lox

            Lox.runtime_error(e)
            return None

    def evaluate(self, expr: "ast.expressions.Expression"):
        return expr.accept(self)

    def execute(self, stmt: "ast.statements.Statement"):
        return stmt.accept(self)

    def visitExpressionStatement(self, stmt: "ast.statements.Expression") -> None:
        self.evaluate(stmt.expr)

    def visitPrintStatement(self, stmt: "ast.statements.Print") -> None:
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))

    def visitUnaryExpression(self, expr: "ast.expressions.Unary"):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.assert_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        raise Exception("Unreachable")

    def visitLiteralExpression(self, expr: "ast.expressions.Literal"):
        return expr.value

    def visitGroupingExpression(self, expr: "ast.expressions.Grouping"):
        return self.evaluate(expr.expr)

    def visitBinaryExpression(self, expr: "ast.expressions.Binary"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.token.type:
            case TokenType.MINUS:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right

                raise RuntimeError(
                    expr.token, "Operands must be two numbers or two strings."
                )
            case TokenType.SLASH:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) * float(right)

            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

            case TokenType.LESS:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) <= float(right)

            case TokenType.GREATER:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.assert_numbers_operand(expr.token, left, right)
                return float(left) >= float(right)

        raise Exception("Unreachable")

    def is_truthy(self, value) -> bool:
        if value in [None, False, 0, ""]:
            return False

        return True

    def is_equal(self, left, right) -> bool:
        return isinstance(left, type(right)) and left == right

    def assert_number_operand(self, operator: "Token", right):
        if isinstance(right, float):
            return

        raise RuntimeError(operator, "Operand must be a number.")

    def assert_numbers_operand(self, operator: "Token", left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, "Operands must be numbers.")

    def stringify(self, value) -> str:
        if value == None:
            return "nil"

        if isinstance(value, float):
            value = str(value)
            if value.endswith(".0"):
                return value[: len(value) - 2]

            return value

        if isinstance(value, bool):
            return "true" if value else "false"

        return str(value)
