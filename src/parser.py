from src.lexer import Lexer
from src.token import Token

import src.ast as ast


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.current_token: Token = None
        self.peak_token: Token = None

        self.errors: list[str] = []

        self._next_token()
        self._next_token()

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
                return None

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
