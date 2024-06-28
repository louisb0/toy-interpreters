from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.lexer import Token

from lox.visitors import ExpressionVisitor, StatementVisitor
from lox.lexer import TokenType
from lox.callable import Callable


class RuntimeError(Exception):
    def __init__(self, token: "Token", message: str):
        super().__init__(message)

        self.token = token


class Interpreter(ExpressionVisitor, StatementVisitor):
    def __init__(self):
        self.env = Environment()

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

    def execute_block(
        self, statements: list["ast.statements.Statement"], env: "Environment"
    ):
        previous = self.env

        try:
            self.env = env

            for statement in statements:
                self.execute(statement)
        finally:
            self.env = previous

    def visitExpressionStatement(self, stmt: "ast.statements.Expression") -> None:
        self.evaluate(stmt.expr)

    def visitBlockStatement(self, stmt: "ast.statements.Block") -> None:
        self.execute_block(stmt.statements, Environment(self.env))

    def visitIfStatement(self, stmt: "ast.statements.If") -> None:
        condition = self.evaluate(stmt.condition)

        if self.is_truthy(condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visitWhileStatement(self, stmt: "ast.statements.While") -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visitPrintStatement(self, stmt: "ast.statements.Print") -> None:
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))

    def visitVarStatement(self, stmt: "ast.statements.Var") -> None:
        value = None
        if stmt.initialiser:
            value = self.evaluate(stmt.initialiser)

        self.env.define(stmt.name.raw, value)

    def visitAssignmentExpression(self, expr: "ast.expressions.Assignment"):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name, value)
        return value

    def visitLogicalExpression(self, expr: "ast.expressions.Logical"):
        left = self.evaluate(expr.left)

        if expr.token.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visitUnaryExpression(self, expr: "ast.expressions.Unary"):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.assert_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        raise Exception("Unreachable")

    def visitVariableExpression(self, expr: "ast.expressions.Variable"):
        return self.env.get(expr.name)

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

    def visitCallExpression(self, expr: "ast.expressions.Call"):
        callee = self.evaluate(expr.callee)

        arguments: list = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, Callable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")

        function: Callable = callee
        if function.arity() != len(arguments):
            raise RuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but received {len(arguments)}.",
            )

        return function.call(self, arguments)

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


class Environment:
    def __init__(self, enclosing: "Environment | None" = None):
        self.enclosing = enclosing

        self.values = {}

    def define(self, name: str, value) -> None:
        self.values[name] = value

    def assign(self, token: "Token", value) -> None:
        if token.raw in self.values:
            self.values[token.raw] = value
            return

        if self.enclosing:
            self.enclosing.assign(token, value)
            return

        raise RuntimeError(token, f"Undefined variable '{token.raw}'.")

    def get(self, token: "Token"):
        if token.raw in self.values:
            return self.values[token.raw]

        if self.enclosing:
            return self.enclosing.get(token)

        raise RuntimeError(token, f"Undefined variable '{token.raw}'.")
