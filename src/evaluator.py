from typing import cast

import src.ast as ast
import src.object as objects


class Evaluator:
    TRUE = objects.Boolean(True)
    FALSE = objects.Boolean(False)
    NULL = objects.Null()

    @staticmethod
    def eval(node: ast.Node) -> objects.Object:
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
                if isinstance(right, objects.Error):
                    return right

                return Evaluator.eval_prefix_expression(node.operator, right)
            case ast.InfixExpression():
                left = Evaluator.eval(node.left)
                if isinstance(left, objects.Error):
                    return left

                right = Evaluator.eval(node.right)
                if isinstance(right, objects.Error):
                    return right

                return Evaluator.eval_infix_expression(left, node.operator, right)

            case ast.BlockStatement():
                return Evaluator.eval_block_statement(node)

            case ast.IfExpression():
                return Evaluator.eval_conditional_expression(node)

            case ast.ReturnStatement():
                value = Evaluator.eval(node.return_value)
                if isinstance(value, objects.Error):
                    return value

                return objects.ReturnValue(value)

        return objects.Error(f"cannot evaluate type: {type(node).__name__}")

    @staticmethod
    def eval_program(program: ast.Program) -> objects.Object:
        result = Evaluator.NULL

        for statement in program.statements:
            result = Evaluator.eval(statement)

            if isinstance(result, objects.ReturnValue):
                return result.value
            elif isinstance(result, objects.Error):
                return result

        return result

    @staticmethod
    def eval_block_statement(block: ast.BlockStatement) -> objects.Object:
        result = Evaluator.NULL

        for statement in block.statements:
            result = Evaluator.eval(statement)

            if isinstance(result, objects.ReturnValue):
                return result
            elif isinstance(result, objects.Error):
                return result

        return result

    @staticmethod
    def eval_prefix_expression(operator: str, right: objects.Object) -> objects.Object:
        match operator:
            case "!":
                return Evaluator._eval_bang_operator_expression(right)
            case "-":
                return Evaluator._eval_minus_operator_expression(right)

        return objects.Error(f"unknown operator: {operator}{right}")

    @staticmethod
    def _eval_bang_operator_expression(right: objects.Object) -> objects.Object:
        if right == Evaluator.TRUE:
            return Evaluator.FALSE
        elif right == Evaluator.FALSE:
            return Evaluator.TRUE
        elif right == Evaluator.NULL:
            return Evaluator.FALSE

        return Evaluator.FALSE

    @staticmethod
    def _eval_minus_operator_expression(right: objects.Object) -> objects.Object:
        if not isinstance(right, objects.Integer):
            return objects.Error(f"unknown operator: -{type(right).__name__}")

        right = cast(objects.Integer, right)
        return objects.Integer(-1 * right.value)

    @staticmethod
    def eval_infix_expression(
        left: objects.Object, operator: str, right: objects.Object | None
    ) -> objects.Object:
        if type(left) != type(right):
            return objects.Error(
                f"type mismatch: {type(left).__name__} {operator} {type(right).__name__}"
            )

        if isinstance(left, objects.Integer) and isinstance(right, objects.Integer):
            left = cast(objects.Integer, left)
            right = cast(objects.Integer, right)

            return Evaluator._eval_integer_infix_expression(left, operator, right)
        elif operator == "==":
            return Evaluator._native_bool_to_obj(left == right)
        elif operator == "!=":
            return Evaluator._native_bool_to_obj(left != right)

        return objects.Error(
            f"unknown operator: {type(left).__name__} {operator} {type(right).__name__}"
        )

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

        return objects.Error(
            f"unknown operator: {type(left).__name__} {operator} {type(right).__name__}"
        )

    @staticmethod
    def eval_conditional_expression(node: ast.IfExpression) -> objects.Object:
        condition = Evaluator.eval(node.condition)
        if isinstance(condition, objects.Error):
            return condition

        if Evaluator._is_truthy(condition):
            return Evaluator.eval(node.consequence)
        elif node.alternative != None:
            return Evaluator.eval(node.alternative)
        else:
            return Evaluator.NULL

    @staticmethod
    def _is_truthy(obj: objects.Object) -> bool:
        if obj == Evaluator.FALSE:
            return False
        elif obj == Evaluator.NULL:
            return False
        else:
            return True

    @staticmethod
    def _native_bool_to_obj(input: bool) -> objects.Boolean:
        return Evaluator.TRUE if input else Evaluator.FALSE
