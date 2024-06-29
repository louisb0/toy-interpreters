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
        return visitor.visitExpressionStatement(self)


class Print(Statement):
    def __init__(self, expr: "ast.expressions.Expression"):
        self.expr = expr

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitPrintStatement(self)


class Var(Statement):
    def __init__(self, name: "Token", initialiser: "ast.expressions.Expression | None"):
        self.name = name
        self.initialiser = initialiser

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitVarStatement(self)


class Block(Statement):
    def __init__(self, statements: list["Statement"]):
        self.statements = statements

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitBlockStatement(self)


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
        return visitor.visitIfStatement(self)


class While(Statement):
    def __init__(self, condition: "ast.expressions.Expression", body: "Statement"):
        self.condition = condition
        self.body = body

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitWhileStatement(self)


class Function(Statement):
    def __init__(self, name: "Token", params: list["Token"], body: "Block"):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitFunctionStatement(self)


class Return(Statement):
    def __init__(self, token: "Token", value: "ast.expressions.Expression | None"):
        self.token = token
        self.value = value

    def accept(self, visitor: "StatementVisitor"):
        return visitor.visitReturnStatement(self)
