from enum import Enum, auto

from src.lexer import Lexer
from src.token import Token

import src.ast as ast


class Precedence(Enum):
    LOWEST = auto()
    EQUALS = auto()  # ==
    LESSGREATER = auto()  # > or <
    SUM = auto()  # +
    PRODUCT = auto()  # *
    PREFIX = auto()  # -X or !X
    CALL = auto()  # myFunction(X)


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token: Token = None
        self.peak_token: Token = None

        self.errors: list[str] = []

        self._next_token()
        self._next_token()

        # TODO: Typing
        self.prefix_parse_functions: dict = {}
        self._register_prefix(Token.IDENT, self._parse_identifier)
        self._register_prefix(Token.INT, self._parse_integer_literal)

        self.infix_parse_functions: dict = {}

    def parse_program(self) -> ast.Program:
        program = ast.Program()

        while self.current_token.token_type != Token.EOF:
            statement = self._parse_statement()
            if statement != None:
                program.statements.append(statement)

            self._next_token()

        return program

    def _parse_statement(self) -> ast.Statement | None:
        match self.current_token.token_type:
            case Token.LET:
                return self._parse_let_statement()
            case Token.RETURN:
                return self._parse_return_statement()
            case _:
                return self._parse_expression_statement()

    def _parse_let_statement(self) -> ast.LetStatement | None:
        statement = ast.LetStatement(self.current_token)

        if not self._expect_peek(Token.IDENT):
            return None

        statement.name = ast.Identifier(self.current_token, self.current_token.literal)

        if not self._expect_peek(Token.ASSIGN):
            return None

        # TODO: Expression parsing. Currently just parsing the token
        # name, need to parse the expression to get the value.
        while self.current_token.token_type != Token.SEMICOLON:
            self._next_token()

        return statement

    def _parse_return_statement(self) -> ast.ReturnStatement | None:
        statement = ast.ReturnStatement(self.current_token)

        self._next_token()

        # TODO: Expression parsing. Currently just parsing the token
        # name, need to parse the expression to get the value.
        while self.current_token.token_type != Token.SEMICOLON:
            self._next_token()

        return statement

    def _parse_expression_statement(self) -> ast.ExpressionStatement:
        statement = ast.ExpressionStatement(self.current_token)

        statement.expression = self._parse_expression(Precedence.LOWEST)

        if self.peak_token.token_type == Token.SEMICOLON:
            self._next_token()

        return statement

    def _parse_expression(self, precedence: Precedence) -> ast.Expression | None:
        prefix = self.prefix_parse_functions[self.current_token.token_type]
        if prefix is None:
            return None

        left_expression = prefix()
        return left_expression

    def _parse_identifier(self) -> ast.Expression:
        return ast.Identifier(self.current_token, self.current_token.literal)

    def _parse_integer_literal(self) -> ast.IntegerLiteral | None:
        literal = ast.IntegerLiteral(self.current_token)

        try:
            parsed_value = int(self.current_token.literal)
        except ValueError:
            self.errors.append(
                f"could not parse {self.current_token.literal} as integer"
            )
            return None

        literal.value = parsed_value
        return literal

    def _register_prefix(self, token_type: str, prefix_parse_function):
        self.prefix_parse_functions[token_type] = prefix_parse_function

    def _register_infix(self, token_type: str, infix_parse_function):
        self.infix_parse_functions[token_type] = infix_parse_function

    def _expect_peek(self, expected: str) -> bool:
        if self.peak_token.token_type == expected:
            self._next_token()
            return True
        else:
            self._peek_error(expected)
            return False

    def _peek_error(self, expected: str):
        self.errors.append(
            f"expected next token to be {expected}, got {self.peak_token.token_type}"
        )

    def _next_token(self) -> None:
        self.current_token = self.peak_token
        self.peak_token = self.lexer.next_token()
