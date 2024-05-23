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
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_boolean_object(evaluated, test["expected"])

    def test_bang_operator(self):
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
