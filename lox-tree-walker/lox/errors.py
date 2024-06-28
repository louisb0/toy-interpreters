from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token

from lox.lexer import TokenType


class ParseError(Exception):
    def __init__(self, token: "Token", message: str):
        super().__init__(message)

        self.token = token
        self.is_eof = token.type == TokenType.EOF


class RuntimeError(Exception):
    def __init__(self, token: "Token", message: str):
        super().__init__(message)

        self.token = token
