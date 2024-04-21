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

        self.assertEqual(len(parser.errors), 0, f"parser errors: {parser.errors}")
        self.assertIsNotNone(program, "parse_program() returned null")
        self.assertEqual(
            len(program.statements),
            3,
            f"program.statements has length {len(program.statements)} != 3",
        )

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

        self.assertEqual(len(parser.errors), 0, f"parser errors: {parser.errors}")
        self.assertIsNotNone(program, "parse_program() returned null")
        self.assertEqual(
            len(program.statements),
            3,
            f"program.statements has length {len(program.statements)} != 3",
        )

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

    def test_identifier_expression(self):
        input = "foobar;"

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()

        self.assertEqual(len(parser.errors), 0, f"parser errors: {parser.errors}")
        self.assertIsNotNone(program, "parse_program() returned null")
        self.assertEqual(
            len(program.statements),
            1,
            f"program.statements has length {len(program.statements)} != 1",
        )

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )
        self.assertIsInstance(
            statement.expression,
            ast.Identifier,
            f"statement.expression is {type(statement.expression).__name__}, expected 'ast.Identifier'",
        )

        identifier: ast.Identifier = statement.expression
        self.assertEqual(
            identifier.value,
            "foobar",
            f"indentifier.value was {identifier.value}, expected 'foobar'",
        )
        self.assertEqual(
            identifier.token_literal(),
            "foobar",
            f"indentifier.token_literal() was {identifier.token_literal()}, expected 'foobar'",
        )

    def test_integer_literal_expression(self):
        input = "5;"

        lexer = Lexer(input)
        parser = Parser(lexer)

        program = parser.parse_program()

        self.assertEqual(len(parser.errors), 0, f"parser errors: {parser.errors}")
        self.assertIsNotNone(program, "parse_program() returned null")
        self.assertEqual(
            len(program.statements),
            1,
            f"program.statements has length {len(program.statements)} != 1",
        )

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )
        self.assertIsInstance(
            statement.expression,
            ast.IntegerLiteral,
            f"statement.expression is {type(statement.expression).__name__}, expected 'ast.IntegerLiteral'",
        )

        integer: ast.IntegerLiteral = statement.expression
        self.assertEqual(
            integer.value,
            5,
            f"integer.value was {integer.value}, expected '5'",
        )
        self.assertEqual(
            integer.token_literal(),
            "5",
            f"integer.token_literal() was {integer.token_literal()}, expected '5'",
        )
