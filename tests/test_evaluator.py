import unittest
from typing import cast

import src.object as objects
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import Evaluator


class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            {"input": "5", "expected": 5},
            {"input": "10", "expected": 10},
            {"input": "-5", "expected": -5},
            {"input": "-10", "expected": -10},
            {"input": "5 + 5 + 5 + 5 - 10", "expected": 10},
            {"input": "2 * 2 * 2 * 2 * 2", "expected": 32},
            {"input": "-50 + 100 + -50", "expected": 0},
            {"input": "5 * 2 + 10", "expected": 20},
            {"input": "5 + 2 * 10", "expected": 25},
            {"input": "20 + 2 * -10", "expected": 0},
            {"input": "50 / 2 * 2 + 10", "expected": 60},
            {"input": "2 * (5 + 10)", "expected": 30},
            {"input": "3 * 3 * 3 + 10", "expected": 37},
            {"input": "3 * (3 * 3) + 10", "expected": 37},
            {"input": "(5 + 10 * 2 + 15 / 3) * 2 + -10", "expected": 50},
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_integer_object(evaluated, test["expected"])

    def test_eval_boolean_expression(self):
        tests = [
            {"input": "true", "expected": True},
            {"input": "false", "expected": False},
            {"input": "1 < 2", "expected": True},
            {"input": "1 > 2", "expected": False},
            {"input": "1 < 1", "expected": False},
            {"input": "1 > 1", "expected": False},
            {"input": "1 == 1", "expected": True},
            {"input": "1 != 1", "expected": False},
            {"input": "1 == 2", "expected": False},
            {"input": "1 != 2", "expected": True},
            {"input": "true == true", "expected": True},
            {"input": "false == false", "expected": True},
            {"input": "true == false", "expected": False},
            {"input": "true != false", "expected": True},
            {"input": "false != true", "expected": True},
            {"input": "(1 < 2) == true", "expected": True},
            {"input": "(1 < 2) == false", "expected": False},
            {"input": "(1 > 2) == true", "expected": False},
            {"input": "(1 > 2) == false", "expected": True},
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_boolean_object(evaluated, test["expected"])

    def test_eval_bang_operator(self):
        tests = [
            {"input": "!true", "expected": False},
            {"input": "!false", "expected": True},
            {"input": "!5", "expected": False},
            {"input": "!!true", "expected": True},
            {"input": "!!false", "expected": False},
            {"input": "!!5", "expected": True},
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_boolean_object(evaluated, test["expected"])

    def test_eval_conditional_expression(self):
        tests = [
            {"input": "if (true) { 10 }", "expected": 10},
            {"input": "if (false) { 10 }", "expected": None},
            {"input": "if (1) { 10 }", "expected": 10},
            {"input": "if (1 < 2) { 10 }", "expected": 10},
            {"input": "if (1 > 2) { 10 }", "expected": None},
            {"input": "if (1 > 2) { 10 } else { 20 }", "expected": 20},
            {"input": "if (1 < 2) { 10 } else { 20 }", "expected": 10},
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])

            if isinstance(test["expected"], int):
                self._test_integer_object(evaluated, test["expected"])
            elif test["expected"] is None:
                self._test_null_object(evaluated)

    def test_eval_return_expression(self):
        tests = [
            {"input": "return 10;", "expected": 10},
            {"input": "return 10; 9;", "expected": 10},
            {"input": "return 2 * 5; 9;", "expected": 10},
            {"input": "9; return 2 * 5; 9;", "expected": 10},
            {
                "input": """
                if (2>1) { 
                    if (2>1) {
                        return 10;
                    } 
                    return 1;
                }
                """,
                "expected": 10,
            },
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_integer_object(evaluated, test["expected"])

    def test_eval_error(self):
        tests = [
            {
                "input": "5 + true;",
                "expected_message": "type mismatch: Integer + Boolean",
            },
            {
                "input": "5 + true; 5;",
                "expected_message": "type mismatch: Integer + Boolean",
            },
            {"input": "-true", "expected_message": "unknown operator: -Boolean"},
            {
                "input": "true + false;",
                "expected_message": "unknown operator: Boolean + Boolean",
            },
            {
                "input": "5; true + false; 5",
                "expected_message": "unknown operator: Boolean + Boolean",
            },
            {
                "input": "if (10 > 1) { true + false; }",
                "expected_message": "unknown operator: Boolean + Boolean",
            },
            {
                "input": """
                if (10 > 1) {
                    if (10 > 1) {
                        return true + false;
                    }
                    return 1;
                }
                """,
                "expected_message": "unknown operator: Boolean + Boolean",
            },
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])

            self.assertIsInstance(
                evaluated,
                objects.Error,
                f"expected objects.Error, got {type(evaluated).__name__}",
            )

            evaluated = cast(objects.Error, evaluated)
            self.assertEqual(evaluated.message, test["expected_message"])

    def _test_eval(self, input: str) -> objects.Object | None:
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        return Evaluator.eval(program)

    def _test_integer_object(self, obj: objects.Object | None, expected: int):
        self.assertIsInstance(
            obj, objects.Integer, f"expected objects.Integer, got {type(obj).__name__}"
        )

        obj = cast(objects.Integer, obj)
        self.assertEqual(
            obj.value,
            expected,
            f"expected objects.Integer to have value {expected}, got {obj.value}",
        )

    def _test_boolean_object(self, obj: objects.Object | None, expected: bool):
        self.assertIsInstance(
            obj, objects.Boolean, f"expected objects.Boolean, got {type(obj).__name__}"
        )

        obj = cast(objects.Boolean, obj)
        self.assertEqual(
            obj.value,
            expected,
            f"expected objects.Boolean to have value {expected}, got {obj.value}",
        )

    def _test_null_object(self, obj: objects.Object | None):
        self.assertEqual(
            obj, Evaluator.NULL, f"expected Evaluator.NULL, got {type(obj).__name__}"
        )
