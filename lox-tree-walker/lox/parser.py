from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token

import lox.ast as ast
from lox.lexer import TokenType


class ParseError(Exception):
    def __init__(self, token: "Token", message: str):
        super().__init__(message)

        self.token = token
        self.is_eof = token.type == TokenType.EOF


class Parser:
    """
    This parser aligns identically with the natural manual parsing
    of an unambiguous regular grammar.

    The job of a parser is to find the composition of grammar rules
    which produced the given string. Precedence and associativty
    are baked into an unambiguous grammar by parsing 'top-down',
    providing the opportunity to match low precedence operators
    early, placing them higher in the tree.

    This parser aligns closely with that grammar definition.
    It is very inefficient however; to parse a literal, you must
    call expression(), equality(), ..., unary(), primary().
    """

    def __init__(self, tokens: list["Token"]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> "ast.Expression | None":
        try:
            return self.expression()
        except ParseError as e:
            from lox import Lox

            Lox.parse_error(e)
            return None

    def expression(self) -> "ast.Expression":
        return self.equality()

    def equality(self) -> "ast.Expression":
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.equality()

            expr = ast.Binary(expr, operator, right)

        return expr

    def comparison(self) -> "ast.Expression":
        expr = self.term()

        while self.match(
            [
                TokenType.LESS,
                TokenType.LESS_EQUAL,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
            ]
        ):
            operator = self.previous()
            right = self.comparison()

            expr = ast.Binary(expr, operator, right)

        return expr

    def term(self) -> "ast.Expression":
        expr = self.factor()

        while self.match([TokenType.PLUS, TokenType.MINUS]):
            operator = self.previous()
            right = self.term()

            expr = ast.Binary(expr, operator, right)

        return expr

    def factor(self) -> "ast.Expression":
        expr = self.unary()

        while self.match([TokenType.STAR, TokenType.SLASH]):
            operator = self.previous()
            right = self.factor()

            expr = ast.Binary(expr, operator, right)

        return expr

    def unary(self) -> "ast.Expression":
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return ast.Unary(operator, right)

        return self.primary()

    def primary(self) -> "ast.Expression":
        if self.match([TokenType.TRUE]):
            return ast.Literal(True)
        elif self.match([TokenType.FALSE]):
            return ast.Literal(False)
        elif self.match([TokenType.NIL]):
            return ast.Literal(None)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return ast.Literal(self.previous().literal)

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return ast.Grouping(expr)

        raise ParseError(self.peek(), "Expected expression.")

    def match(self, token_types: list["TokenType"]) -> bool:
        for type in token_types:
            if self.check(type):
                self.advance()
                return True

        return False

    def check(self, type: "TokenType") -> bool:
        if self.is_at_end():
            return False

        return self.peek().type == type

    def advance(self) -> "Token":
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek() == TokenType.EOF

    def peek(self) -> "Token":
        return self.tokens[self.current]

    def previous(self) -> "Token":
        return self.tokens[self.current - 1]

    def consume(self, expected: "TokenType", message: str) -> "Token":
        if self.check(expected):
            return self.advance()

        raise ParseError(self.peek(), message)

    def synchronise(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            self.advance()
