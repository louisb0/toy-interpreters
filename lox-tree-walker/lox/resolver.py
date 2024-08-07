from collections import deque
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.interpreter import Interpreter
    from lox.lexer import Token

import lox.ast as ast
from lox.visitors import ExpressionVisitor, StatementVisitor
from lox import Lox
from lox.errors import ParseError


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()
    INITIALISER = auto()


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()


class Resolver(ExpressionVisitor, StatementVisitor):
    def __init__(self, interpreter: "Interpreter"):
        self.interpreter = interpreter

        # stack of dict[str, bool]
        self.scopes = deque()
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE

    def resolve_statements(self, statements: list["ast.statements.Statement"]):
        for statement in statements:
            self.resolve_statement(statement)

    def resolve_statement(self, statement: "ast.statements.Statement"):
        statement.accept(self)

    def resolve_expression(self, expression: "ast.expressions.Expression"):
        expression.accept(self)

    def resolve_local(self, expr: "ast.expressions.Expression", name: "Token"):
        for i in range(len(self.scopes) - 1, -1, -1):
            if self.scopes[i].get(name.raw) is not None:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, stmt: "ast.statements.Function", type: "FunctionType"):
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()

        for param in stmt.params:
            self.declare(param)
            self.define(param)

        self.resolve_statements(stmt.body.statements)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: "Token"):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        if name.raw in scope:
            Lox.parse_error(
                ParseError(name, "Already a variable with this name in this scope.")
            )

        scope[name.raw] = False

    def define(self, name: "Token"):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.raw] = True

    def visit_block_statement(self, stmt: "ast.statements.Block"):
        self.begin_scope()
        self.resolve_statements(stmt.statements)
        self.end_scope()

    def visit_var_statement(self, stmt: "ast.statements.Var"):
        self.declare(stmt.name)

        if stmt.initialiser:
            self.resolve_expression(stmt.initialiser)

        self.define(stmt.name)

    def visit_variable_expression(self, expr: "ast.expressions.Variable"):
        if len(self.scopes) > 0 and self.scopes[-1].get(expr.name.raw) == False:
            Lox.parse_error(
                ParseError(
                    expr.name, "Can't read local variable in it's own initialiser."
                )
            )

        self.resolve_local(expr, expr.name)

    def visit_assignment_expression(self, expr: "ast.expressions.Assignment"):
        self.resolve_expression(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_function_statement(self, stmt: "ast.statements.Function"):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_class_statement(self, stmt: "ast.statements.Class"):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass and stmt.superclass.name.raw == stmt.name.raw:
            Lox.parse_error(
                ParseError(stmt.superclass.name, "A class can't inherit from itself.")
            )

        if stmt.superclass:
            self.current_class = ClassType.SUBCLASS
            self.resolve_expression(stmt.superclass)

        if stmt.superclass:
            self.begin_scope()
            self.scopes[-1]["super"] = True

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if method.name.raw == "init":
                declaration = FunctionType.INITIALISER

            self.resolve_function(method, declaration)

        self.end_scope()

        if stmt.superclass:
            self.end_scope()

        self.current_class = enclosing_class

    """ Unaffected by variable resolution below, but needed for traversal """

    def visit_expression_statement(self, stmt: "ast.statements.Expression") -> None:
        self.resolve_expression(stmt.expr)

    def visit_print_statement(self, stmt: "ast.statements.Print") -> None:
        self.resolve_expression(stmt.expr)

    def visit_if_statement(self, stmt: "ast.statements.If") -> None:
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.then_branch)

        if stmt.else_branch:
            self.resolve_statement(stmt.else_branch)

    def visit_while_statement(self, stmt: "ast.statements.While") -> None:
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.body)

    def visit_return_statement(self, stmt: "ast.statements.Return") -> None:
        if self.current_function == FunctionType.NONE:
            Lox.parse_error(ParseError(stmt.token, "Can't return from top-level code."))

        if stmt.value:
            if self.current_function == FunctionType.INITIALISER:
                Lox.parse_error(
                    ParseError(stmt.token, "Can't return a value from an initialiser.")
                )

            self.resolve_expression(stmt.value)

    def visit_unary_expression(self, expr: "ast.expressions.Unary"):
        self.resolve_expression(expr.right)

    def visit_literal_expression(self, expr: "ast.expressions.Literal"):
        return

    def visit_grouping_expression(self, expr: "ast.expressions.Grouping"):
        self.resolve_expression(expr.expr)

    def visit_binary_expression(self, expr: "ast.expressions.Binary"):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)

    def visit_logical_expression(self, expr: "ast.expressions.Logical"):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)

    def visit_call_expression(self, expr: "ast.expressions.Call"):
        self.resolve_expression(expr.callee)

        for arg in expr.arguments:
            self.resolve_expression(arg)

    def visit_get_expression(self, expr: "ast.expressions.Get"):
        self.resolve_expression(expr.object)

    def visit_set_expression(self, expr: "ast.expressions.Set"):
        self.resolve_expression(expr.object)
        self.resolve_expression(expr.value)

    def visit_this_expression(self, expr: "ast.expressions.This"):
        if self.current_class == ClassType.NONE:
            Lox.parse_error(
                ParseError(
                    expr.keyword, "Can't reference 'this' from outside a class method."
                )
            )

        self.resolve_local(expr, expr.keyword)

    def visit_super_expression(self, expr: "ast.expressions.Super"):
        if self.current_class == ClassType.NONE:
            Lox.parse_error(
                ParseError(
                    expr.keyword, "Can't reference 'super' from outside a class method."
                )
            )
        elif self.current_class != ClassType.SUBCLASS:
            Lox.parse_error(
                ParseError(
                    expr.keyword, "Can't reference 'super' without a superclass."
                )
            )

        self.resolve_local(expr, expr.keyword)
