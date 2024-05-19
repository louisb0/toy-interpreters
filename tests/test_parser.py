import unittest
from typing import cast

from src.lexer import Lexer
from src.parser import Parser
import src.ast as ast

# TODO: multiple classes wtf is this


class TestParser(unittest.TestCase):
    def test_let_statements(self):
        tests = [
            {"input": "let x = 5;", "expected_identifier": "x", "expected_value": 5},
            {"input": "let y = 10;", "expected_identifier": "y", "expected_value": 10},
            {
                "input": "let foobar = 83812;",
                "expected_identifier": "foobar",
                "expected_value": 83812,
            },
        ]

        for test in tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, num_expected_statements=1)

            statement = program.statements[0]
            self._test_let_statement(statement, test["expected_identifier"])

            statement = cast(ast.LetStatement, statement)
            self._test_literal_expression(statement.value, test["expected_value"])

    def test_return_statements(self):
        input = """return 5;
return 10;
return 123123;"""

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self._test_parser_state(parser, program, num_expected_statements=3)

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
        self._test_parser_state(parser, program, num_expected_statements=1)

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )
        statement = cast(ast.ExpressionStatement, statement)
        self._test_identifier(statement.expression, "foobar")

    def test_integer_literal_expression(self):
        input = "5;"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self._test_parser_state(parser, program, num_expected_statements=1)

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )

        self._test_integer_literal(statement.expression, 5)

    def test_boolean_expression(self):
        boolean_tests = [
            {"input": "true", "value": True},
            {"input": "false;", "value": False},
        ]

        for test in boolean_tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, num_expected_statements=1)

            statement = program.statements[0]
            self.assertIsInstance(
                statement,
                ast.ExpressionStatement,
                f"program.statements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
            )
            self._test_boolean_literal(statement.expression, test["value"])

    def test_prefix_expressions(self):
        prefix_tests = [
            {"input": "!5", "operator": "!", "value": 5},
            {"input": "-15", "operator": "-", "value": 15},
            {"input": "!true", "operator": "!", "value": True},
            {"input": "!false", "operator": "!", "value": False},
        ]

        for test in prefix_tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, num_expected_statements=1)

            statement = program.statements[0]
            self.assertIsInstance(
                statement,
                ast.ExpressionStatement,
                f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
            )
            self.assertIsInstance(
                statement.expression,
                ast.PrefixExpression,
                f"statement.expression is {type(statement.expression).__name__}, expected 'ast.PrefixExpresion'",
            )

            self.assertEqual(
                statement.expression.operator,
                test["operator"],
                f"statement.expression.operator is {statement.expression.operator}, expected '{test['operator']}'",
            )

            self._test_literal_expression(statement.expression.right, test["value"])

    def test_infix_expressions(self):
        infix_tests = [
            {"input": "5 + 5;", "left_value": 5, "operator": "+", "right_value": 5},
            {"input": "5 - 5;", "left_value": 5, "operator": "-", "right_value": 5},
            {"input": "5 * 5;", "left_value": 5, "operator": "*", "right_value": 5},
            {"input": "5 / 5;", "left_value": 5, "operator": "/", "right_value": 5},
            {"input": "5 > 5;", "left_value": 5, "operator": ">", "right_value": 5},
            {"input": "5 < 5;", "left_value": 5, "operator": "<", "right_value": 5},
            {"input": "5 == 5;", "left_value": 5, "operator": "==", "right_value": 5},
            {"input": "5 != 5;", "left_value": 5, "operator": "!=", "right_value": 5},
            {
                "input": "true == true",
                "left_value": True,
                "operator": "==",
                "right_value": True,
            },
            {
                "input": "true != false",
                "left_value": True,
                "operator": "!=",
                "right_value": False,
            },
            {
                "input": "false == false",
                "left_value": False,
                "operator": "==",
                "right_value": False,
            },
        ]

        for test in infix_tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, num_expected_statements=1)

            statement = program.statements[0]
            self.assertIsInstance(
                statement,
                ast.ExpressionStatement,
                f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
            )

            self._test_infix_expression(
                statement.expression,
                test["left_value"],
                test["operator"],
                test["right_value"],
            )

    def test_operator_precedence(self):
        tests = [
            {"input": "-a * b", "expected_output": "((-a) * b)"},
            {"input": "!-a", "expected_output": "(!(-a))"},
            {"input": "a + b + c", "expected_output": "((a + b) + c)"},
            {"input": "a + b - c", "expected_output": "((a + b) - c)"},
            {"input": "a * b * c", "expected_output": "((a * b) * c)"},
            {"input": "a * b / c", "expected_output": "((a * b) / c)"},
            {"input": "a + b / c", "expected_output": "(a + (b / c))"},
            {
                "input": "a + b * c + d / e - f",
                "expected_output": "(((a + (b * c)) + (d / e)) - f)",
            },
            {"input": "3 + 4; -5 * 5", "expected_output": "(3 + 4)((-5) * 5)"},
            {"input": "5 > 4 == 3 < 4", "expected_output": "((5 > 4) == (3 < 4))"},
            {"input": "5 < 4 != 3 > 4", "expected_output": "((5 < 4) != (3 > 4))"},
            {
                "input": "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "expected_output": "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
            },
            {
                "input": "3 + 4 * 5 == 3 * 1 + 4 * 5",
                "expected_output": "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
            },
            {"input": "true", "expected_output": "true"},
            {"input": "false", "expected_output": "false"},
            {"input": "3 > 5 == false", "expected_output": "((3 > 5) == false)"},
            {"input": "3 < 5 == true", "expected_output": "((3 < 5) == true)"},
            {"input": "1 + (2 + 3) + 4", "expected_output": "((1 + (2 + 3)) + 4)"},
            {"input": "(5 + 5) * 2", "expected_output": "((5 + 5) * 2)"},
            {"input": "2 / (5 + 5)", "expected_output": "(2 / (5 + 5))"},
            {"input": "-(5 + 5)", "expected_output": "(-(5 + 5))"},
            {"input": "!(true == true)", "expected_output": "(!(true == true))"},
        ]

        for test in tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program)

            self.assertEqual(str(program), test["expected_output"])

    def test_if_else_expression(self):
        input = "if (x < y) { x } else { y }"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self._test_parser_state(parser, program)

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )

        self.assertIsInstance(
            statement.expression,
            ast.IfExpression,
            f"expression is {type(statement).__name__}, expected 'ast.IfExpression",
        )

        if_expression: ast.IfExpression = statement.expression
        self._test_infix_expression(if_expression.condition, "x", "<", "y")

        self.assertEqual(
            len(if_expression.consequence.statements),
            1,
            "expression.consequence.statements has length != 1",
        )
        consequence: ast.Expression = if_expression.consequence.statements[0].expression
        self._test_identifier(consequence, "x")

        self.assertEqual(
            len(if_expression.alternative.statements),
            1,
            "expression.alternative.statements has length != 1",
        )
        alternative: ast.Expression = if_expression.alternative.statements[0].expression
        self._test_identifier(alternative, "y")

    def test_function_literal(self):
        input = "fn (x, y) { x + y; }"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self._test_parser_state(parser, program, 1)

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )

        self.assertIsInstance(
            statement.expression,
            ast.FunctionLiteral,
            f"expression is {type(statement).__name__}, expected 'ast.FunctionLiteral",
        )

        func: ast.FunctionLiteral = statement.expression

        self.assertEqual(
            len(func.parameters),
            2,
            f"function has {len(func.parameters)} parameters, expected 2",
        )

        self._test_identifier(func.parameters[0], "x")
        self._test_identifier(func.parameters[1], "y")

        self.assertEqual(
            len(func.body.statements),
            1,
            f"block statement has {len(func.body.statements)} statements, expected 1",
        )

        self.assertIsInstance(
            func.body.statements[0].expression,
            ast.InfixExpression,
            f"block statement contians {type(func.body.statements[0]).__name__}, expected ast.InfixExpression",
        )

        body: ast.InfixExpression = func.body.statements[0].expression
        self._test_infix_expression(body, "x", "+", "y")

    def test_function_literal_parameters(self):
        tests = [
            {"input": "fn() {};", "expected_params": []},
            {"input": "fn(x) {};", "expected_params": ["x"]},
            {"input": "fn(x, y, z) {};", "expected_params": ["x", "y", "z"]},
        ]

        for test in tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, 1)

            fn: ast.FunctionLiteral = program.statements[0].expression
            self.assertEqual(
                len(fn.parameters),
                len(test["expected_params"]),
                f"expected function to have {test['expected_params']}, got {len(fn.parameters)}",
            )
            for i, identifier in enumerate(test["expected_params"]):
                self._test_literal_expression(fn.parameters[i], identifier)

    def test_call_expression(self):
        input = "add(1, 2 * 3, 4 + 5);"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.parse_program()
        self._test_parser_state(parser, program, 1)

        statement = program.statements[0]
        self.assertIsInstance(
            statement,
            ast.ExpressionStatement,
            f"program.statemements[0] is {type(statement).__name__}, expected 'ast.ExpressionStatement",
        )
        self.assertIsInstance(
            statement.expression,
            ast.CallExpression,
            f"program.statemements[0].expression is {type(statement.expression).__name__}, expected 'ast.CallExpression",
        )

        call: ast.CallExpression = statement.expression
        self._test_identifier(call.expression, "add")
        self.assertEqual(
            len(call.arguments),
            3,
            f"expected call expression to have 3 arguments, got {len(call.arguments)}",
        )

        self._test_literal_expression(call.arguments[0], 1)
        self._test_infix_expression(call.arguments[1], 2, "*", 3)
        self._test_infix_expression(call.arguments[2], 4, "+", 5)

    def test_call_expression_parameters(self):
        tests = [
            {"input": "add();", "expected_params": []},
            {"input": "add(x);", "expected_params": ["x"]},
            {"input": "add(x, y, z);", "expected_params": ["x", "y", "z"]},
        ]

        for test in tests:
            lexer = Lexer(test["input"])
            parser = Parser(lexer)
            program = parser.parse_program()
            self._test_parser_state(parser, program, 1)

            call: ast.CallExpression = program.statements[0].expression
            self.assertEqual(
                len(call.arguments),
                len(test["expected_params"]),
                f"expected call expression to have {test['expected_params']}, got {len(call.arguments)}",
            )
            for i, identifier in enumerate(test["expected_params"]):
                self._test_literal_expression(call.arguments[i], identifier)

    def _test_parser_state(
        self,
        parser: Parser,
        program: ast.Program,
        num_expected_statements: int | None = None,
    ):
        self.assertEqual(len(parser.errors), 0, f"parser errors: {parser.errors}")
        self.assertIsNotNone(program, "parse_program() returned null")

        if num_expected_statements is not None:
            self.assertEqual(
                len(program.statements),
                num_expected_statements,
                f"program.statements has length {len(program.statements)} != {num_expected_statements}",
            )

    def _test_infix_expression(
        self,
        expression: ast.Expression,
        left,
        operator: str,
        right,
    ):
        self.assertIsInstance(
            expression,
            ast.InfixExpression,
            f"expression is {type(expression).__name__}, expected 'ast.InfixExpresion'",
        )

        self._test_literal_expression(expression.left, left)

        self.assertEqual(
            expression.operator,
            operator,
            f"expression.operator is {expression.operator}, expected '{operator}'",
        )

        self._test_literal_expression(expression.right, right)

    def _test_literal_expression(
        self, expression: ast.Expression, expected: int | str | bool
    ):
        match expected:
            case bool():
                self._test_boolean_literal(expression, expected)
            case int():
                self._test_integer_literal(expression, expected)
            case str():
                self._test_identifier(expression, expected)
            case _:
                self.fail(
                    f"type of expression '{type(expression).__name__}' not handled"
                )

    def _test_integer_literal(self, expression: ast.Expression, expected: int):
        self.assertIsInstance(
            expression,
            ast.IntegerLiteral,
            f"statement.expression is {type(expression).__name__}, expected 'ast.IntegerLiteral'",
        )

        integer: ast.IntegerLiteral = expression
        self.assertEqual(
            integer.value,
            expected,
            f"integer.value was {integer.value}, expected '{expected}'",
        )
        self.assertEqual(
            integer.token_literal(),
            str(expected),
            f"integer.token_literal() was {integer.token_literal()}, expected '{expected}'",
        )

    def _test_identifier(self, expression: ast.Expression, value: str):
        self.assertIsInstance(
            expression,
            ast.Identifier,
            f"expression was {type(expression).__name__}, expected 'ast.Identifier'",
        )

        identifier: ast.Identifier = expression
        self.assertEqual(
            identifier.value,
            value,
            f"indentifier.value was {identifier.value}, expected '{value}'",
        )
        self.assertEqual(
            identifier.token_literal(),
            value,
            f"indentifier.token_literal() was {identifier.token_literal()}, expected '{value}'",
        )

    def _test_boolean_literal(self, expression: ast.Expression, value: bool):
        self.assertIsInstance(
            expression,
            ast.Boolean,
            f"statement.expression is {type(expression).__name__}, expected 'ast.Boolean",
        )

        boolean = cast(ast.Boolean, expression)
        self.assertEqual(
            boolean.value,
            value,
            f"boolean.value was {boolean.value}, expected '{value}'",
        )
        self.assertEqual(
            boolean.token_literal(),
            str(value).lower(),  # python sux
            f"boolean.token_literal() was {boolean.token_literal()}, expected '{value}'",
        )

    def _test_let_statement(self, statement: ast.Statement, name: str):
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

        let_statement = cast(ast.LetStatement, statement)
        self.assertEqual(
            let_statement.name.value,
            name,
            f"LetStatement.name.value is {let_statement.name.value}, expected '{name}'",
        )
        self.assertEqual(
            let_statement.name.token_literal(),
            name,
            f"let_statement.name.token_literal() is {statement.name.token_literal()}, expected '{name}'",
        )
