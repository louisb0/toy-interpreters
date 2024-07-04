from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.lexer import Token

from lox.visitors import ExpressionVisitor, StatementVisitor
from lox.lexer import TokenType
from lox.errors import RuntimeError
from lox.objects import Environment, Class
from lox.objects.callables import Callable, Function, NativeClock, Return


class Interpreter(ExpressionVisitor, StatementVisitor):
    def __init__(self):
        self.globals = Environment()
        self.globals.define("clock", NativeClock())
        self.locals: dict["ast.expressions.Expression", int] = {}

        self.env = self.globals

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

    def resolve(self, expr: "ast.expressions.Expression", depth: int):
        self.locals[expr] = depth

    def look_up_variable(self, name: "Token", expr: "ast.expressions.Expression"):
        distance = self.locals.get(expr)

        if distance is not None:
            return self.env.get_at(distance, name.raw)
        else:
            return self.globals.get(name)

    def execute_block(self, block: "ast.statements.Block", env: "Environment"):
        previous = self.env

        try:
            self.env = env

            for statement in block.statements:
                self.execute(statement)
        finally:
            self.env = previous

    def visit_expression_statement(self, stmt: "ast.statements.Expression") -> None:
        self.evaluate(stmt.expr)

    def visit_class_statement(self, stmt: "ast.statements.Class") -> None:
        self.env.define(stmt.name.raw, None)
        klass = Class(stmt.name.raw)
        self.env.assign(stmt.name, klass)

    def visit_function_statement(self, stmt: "ast.statements.Function") -> None:
        function = Function(stmt, closure=self.env)
        self.env.define(stmt.name.raw, function)

    def visit_block_statement(self, stmt: "ast.statements.Block") -> None:
        self.execute_block(stmt, Environment(self.env))

    def visit_if_statement(self, stmt: "ast.statements.If") -> None:
        condition = self.evaluate(stmt.condition)

        if self.is_truthy(condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch:
            self.execute(stmt.else_branch)

    def visit_while_statement(self, stmt: "ast.statements.While") -> None:
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_print_statement(self, stmt: "ast.statements.Print") -> None:
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))

    def visit_return_statement(self, stmt: "ast.statements.Return") -> None:
        raise Return(self.evaluate(stmt.value) if stmt.value else None)

    def visit_var_statement(self, stmt: "ast.statements.Var") -> None:
        value = None
        if stmt.initialiser:
            value = self.evaluate(stmt.initialiser)

        self.env.define(stmt.name.raw, value)

    def visit_assignment_expression(self, expr: "ast.expressions.Assignment"):
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr)
        if distance is not None:
            self.env.assign_at(distance, expr.name.raw, value)
        else:
            self.globals.assign(expr.name, value)

        return value

    def visit_logical_expression(self, expr: "ast.expressions.Logical"):
        left = self.evaluate(expr.left)

        if expr.token.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_unary_expression(self, expr: "ast.expressions.Unary"):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.assert_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        raise Exception("Unreachable")

    def visit_variable_expression(self, expr: "ast.expressions.Variable"):
        return self.look_up_variable(expr.name, expr)

    def visit_literal_expression(self, expr: "ast.expressions.Literal"):
        return expr.value

    def visit_grouping_expression(self, expr: "ast.expressions.Grouping"):
        return self.evaluate(expr.expr)

    def visit_binary_expression(self, expr: "ast.expressions.Binary"):
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

    def visit_call_expression(self, expr: "ast.expressions.Call"):
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
