from lox.visitors import Visitor
import lox.ast as ast

class TreePrinter(Visitor):
    def print(self, expr: ast.Expression):
        return expr.accept(self)

    def visitUnaryExpression(self, expr: ast.Unary) -> str:
        return f"{expr.operator.raw}({expr.right.accept(self)})"

    def visitLiteralExpression(self, expr: ast.Literal) -> str:
        return str(expr.value)

    def visitGroupingExpression(self, expr: ast.Grouping) -> str:
        return f"(group: {expr.expr.accept(self)})"

    def visitBinaryExpression(self, expr: ast.Binary) -> str:
        return f"({expr.left.accept(self)} {expr.token.raw} ({expr.right.accept(self)}))"
