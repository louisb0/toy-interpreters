import src.ast as ast
import src.object as objects


def eval(node: ast.Node) -> objects.Object | None:
    match node:
        case ast.Program():
            return eval_statements(node.statements)
        case ast.ExpressionStatement():
            return eval(node.expression)

        case ast.IntegerLiteral():
            return objects.Integer(node.value)
        case ast.Boolean():
            return objects.Boolean(node.value)

    return None


def eval_statements(statements: list[ast.Statement]) -> objects.Object | None:
    result = None

    for statement in statements:
        result = eval(statement)

    return result
