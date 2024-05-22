import src.ast as ast
import src.object as objects

TRUE = objects.Boolean(True)
FALSE = objects.Boolean(False)
NULL = objects.Null()


def eval(node: ast.Node) -> objects.Object | None:
    match node:
        case ast.Program():
            return eval_statements(node.statements)
        case ast.ExpressionStatement():
            return eval(node.expression)

        case ast.IntegerLiteral():
            return objects.Integer(node.value)
        case ast.Boolean():
            return _native_bool_to_obj(node.value)

    return None


def eval_statements(statements: list[ast.Statement]) -> objects.Object | None:
    result = None

    for statement in statements:
        result = eval(statement)

    return result


def _native_bool_to_obj(input: bool) -> objects.Boolean:
    return TRUE if input else FALSE
