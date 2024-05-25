from typing import cast

import src.ast as ast
import src.object as objects

# .type() needs to be switched for instanceof


class Evaluator:
    TRUE = objects.Boolean(True)
    FALSE = objects.Boolean(False)
    NULL = objects.Null()

    @staticmethod
    def eval(node: ast.Node) -> objects.Object | None:
        match node:
            case ast.Program():
                return Evaluator.eval_program(node)
            case ast.ExpressionStatement():
                return Evaluator.eval(node.expression)

            case ast.IntegerLiteral():
                return objects.Integer(node.value)
            case ast.Boolean():
                return Evaluator._native_bool_to_obj(node.value)

            case ast.PrefixExpression():
                right = Evaluator.eval(node.right)
                return Evaluator.eval_prefix_expression(node.operator, right)
            case ast.InfixExpression():
                left = Evaluator.eval(node.left)
                right = Evaluator.eval(node.right)
                return Evaluator.eval_infix_expression(left, node.operator, right)

            case ast.BlockStatement():
                return Evaluator.eval_block_statement(node)

            case ast.IfExpression():
                return Evaluator.eval_conditional_expression(node)

            case ast.ReturnStatement():
                value = Evaluator.eval(node.return_value)
                return objects.ReturnValue(value)

        return None

    @staticmethod
    def eval_program(program: ast.Program) -> objects.Object | None:
        result = None

        for statement in program.statements:
            result = Evaluator.eval(statement)

            if isinstance(result, objects.ReturnValue):
                return result.value

        return result

    @staticmethod
    def eval_block_statement(block: ast.BlockStatement) -> objects.Object | None:
        result = None

        for statement in block.statements:
            result = Evaluator.eval(statement)

            if isinstance(result, objects.ReturnValue):
                return result

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
        if not right or right.type() != objects.ObjectTypes.INTEGER:
            return Evaluator.NULL

        right = cast(objects.Integer, right)
        return objects.Integer(-1 * right.value)

    @staticmethod
    def eval_infix_expression(
        left: objects.Object | None, operator: str, right: objects.Object | None
    ) -> objects.Object:
        if not left or not right:
            return Evaluator.NULL

        if (
            left.type() == objects.ObjectTypes.INTEGER
            and right.type() == objects.ObjectTypes.INTEGER
        ):
            left = cast(objects.Integer, left)
            right = cast(objects.Integer, right)

            return Evaluator._eval_integer_infix_expression(left, operator, right)
        elif operator == "==":
            return Evaluator._native_bool_to_obj(left == right)
        elif operator == "!=":
            return Evaluator._native_bool_to_obj(left != right)

        return Evaluator.NULL

    @staticmethod
    def _eval_integer_infix_expression(
        left: objects.Integer, operator: str, right: objects.Integer
    ) -> objects.Object:
        match operator:
            case "+":
                return objects.Integer(left.value + right.value)
            case "-":
                return objects.Integer(left.value - right.value)
            case "*":
                return objects.Integer(left.value * right.value)
            case "/":
                return objects.Integer(left.value // right.value)
            case "<":
                return Evaluator._native_bool_to_obj(left.value < right.value)
            case ">":
                return Evaluator._native_bool_to_obj(left.value > right.value)
            case "==":
                return Evaluator._native_bool_to_obj(left.value == right.value)
            case "!=":
                return Evaluator._native_bool_to_obj(left.value != right.value)

        return Evaluator.NULL

    @staticmethod
    def eval_conditional_expression(node: ast.IfExpression) -> objects.Object | None:
        condition = Evaluator.eval(node.condition)

        if Evaluator._is_truthy(condition):
            return Evaluator.eval(node.consequence)
        elif node.alternative != None:
            return Evaluator.eval(node.alternative)
        else:
            return Evaluator.NULL

    @staticmethod
    def _is_truthy(obj: objects.Object | None) -> bool:
        if obj == Evaluator.FALSE:
            return False
        elif obj == Evaluator.NULL:
            return False
        else:
            return True

    @staticmethod
    def _native_bool_to_obj(input: bool) -> objects.Boolean:
        return Evaluator.TRUE if input else Evaluator.FALSE
