from typing import cast

import src.ast as ast
import src.object as objects


class Evaluator:
    TRUE = objects.Boolean(True)
    FALSE = objects.Boolean(False)
    NULL = objects.Null()

    @staticmethod
    def eval(node: ast.Node) -> objects.Object | None:
        match node:
            case ast.Program():
                return Evaluator.eval_statements(node.statements)
            case ast.ExpressionStatement():
                return Evaluator.eval(node.expression)

            case ast.IntegerLiteral():
                return objects.Integer(node.value)
            case ast.Boolean():
                return Evaluator._native_bool_to_obj(node.value)

            case ast.PrefixExpression():
                right = Evaluator.eval(node.right)
                return Evaluator.eval_prefix_expression(node.operator, right)

        return None

    @staticmethod
    def eval_statements(statements: list[ast.Statement]) -> objects.Object | None:
        result = None

        for statement in statements:
            result = Evaluator.eval(statement)

        return result

    @staticmethod
    def eval_prefix_expression(
        operator: str, right: objects.Object | None
    ) -> objects.Object:
        match operator:
            case "!":
                return Evaluator._eval_bang_operator_expression(right)
            case "-":
                return Evaluator._eval_minus_operator_expression(right)

        return Evaluator.NULL

    @staticmethod
    def _eval_bang_operator_expression(right: objects.Object | None) -> objects.Object:
        if right == Evaluator.TRUE:
            return Evaluator.FALSE
        elif right == Evaluator.FALSE:
            return Evaluator.TRUE
        elif right == Evaluator.NULL:
            return Evaluator.FALSE

        return Evaluator.FALSE

    @staticmethod
    def _eval_minus_operator_expression(right: objects.Object | None) -> objects.Object:
        if right.type() != objects.ObjectTypes.INTEGER:
            return Evaluator.NULL

        right = cast(objects.Integer, right)
        return objects.Integer(-1 * right.value)

    @staticmethod
    def _native_bool_to_obj(input: bool) -> objects.Boolean:
        return Evaluator.TRUE if input else Evaluator.FALSE
