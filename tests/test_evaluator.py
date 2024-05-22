import unittest
from typing import cast

import src.object as objects
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import eval


class TestEvaluator(unittest.TestCase):
    def test_eval_integer_expression(self):
        tests = [
            {"input": "5", "expected": 5},
            {"input": "10", "expected": 10},
        ]

        for test in tests:
            evaluated = self._test_eval(test["input"])
            self._test_integer_object(evaluated, test["expected"])

    def _test_eval(self, input: str) -> objects.Object | None:
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()

        return eval(program)

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
