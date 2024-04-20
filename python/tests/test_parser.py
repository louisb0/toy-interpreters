import unittest

from src.lexer import Lexer
from src.parser import Parser

import src.ast as ast


class TestParser(unittest.TestCase):
    def test_let_statements(self):
        input = """let x = 5;
let y = 10; 
let foobar = 83812;"""

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        if program == None:
            self.fail("parse_program() returned null")

        if len(program.statements) != 3:
            self.fail(f"program.statements has length {len(program.statements)} != 3")

        tests = [
            {"expected_identifier": "x"},
            {"expected_identifier": "y"},
            {"expected_identifier": "foobar"},
        ]
        for i, test in enumerate(tests):
            statement = program.statements[i]
            self._test_let_statement(statement, test["expected_identifier"])

    def _test_let_statement(self, statement: ast.Statement, expected_identifier: str):
        self.assertEqual(
            statement.token_literal(),
            "let",
            f"statement.token_literal() is {statement.token_literal()}, expected 'let'",
        )
        self.assertIsInstance(
            statement,
            ast.LetStatement,
            f"statement is {type(statement).__name__}, expected LetStatement",
        )
        self.assertEqual(
            statement.name.value,
            expected_identifier,
            f"LetStatement.name.value is {statement.name.value}, expected '{expected_identifier}'",
        )
        self.assertEqual(
            statement.name.token_literal(),
            expected_identifier,
            f"statement.name.token_literal() is {statement.name.token_literal()}, expected '{expected_identifier}'",
        )

    def test_return_statements(self):
        input = """return 5;
return 10;
return 123123;"""

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()
        self._check_parser_errors(parser)

        if program == None:
            self.fail("parse_program() returned null")

        if len(program.statements) != 3:
            self.fail(f"program.statements has length {len(program.statements)} != 3")

        for statement in program.statements:
            self.assertIsInstance(
                statement,
                ast.ReturnStatement,
                f"statement is {type(statement).__name__}, expected ReturnStatement",
            )

            self.assertEqual(
                statement.token_literal(),
                "return",
                f"statement.token_literal() is {statement.token_literal()}, expected 'return'",
            )

    def _check_parser_errors(self, parser: Parser):
        if len(parser.errors) == 0:
            return

        self.fail(f"parser errors: {parser.errors}")
