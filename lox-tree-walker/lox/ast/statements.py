from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.visitors import StatementVisitor
    from lox.lexer import Token


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: "StatementVisitor"):
        raise NotImplementedError()


class Expression(Statement):
    def __init__(self, expr: "ast.expressions.Expression"):
        self.expr = expr

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_expression_statement(self)


class Print(Statement):
    def __init__(self, expr: "ast.expressions.Expression"):
        self.expr = expr

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_print_statement(self)


class Var(Statement):
    def __init__(self, name: "Token", initialiser: "ast.expressions.Expression | None"):
        self.name = name
        self.initialiser = initialiser

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_var_statement(self)


class Block(Statement):
    def __init__(self, statements: list["Statement"]):
        self.statements = statements

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_block_statement(self)


class If(Statement):
    def __init__(
        self,
        condition: "ast.expressions.Expression",
        then_branch: "Statement",
        else_branch: "Statement | None",
    ):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_if_statement(self)


class While(Statement):
    def __init__(self, condition: "ast.expressions.Expression", body: "Statement"):
        self.condition = condition
        self.body = body

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_while_statement(self)


class Function(Statement):
    def __init__(self, name: "Token", params: list["Token"], body: "Block"):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_function_statement(self)


class Return(Statement):
    def __init__(self, token: "Token", value: "ast.expressions.Expression | None"):
        self.token = token
        self.value = value

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_return_statement(self)


class Class(Statement):
    def __init__(
        self,
        name: "Token",
        superclass: "ast.expressions.Variable | None",
        methods: list["Function"],
    ):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visit_class_statement(self)
