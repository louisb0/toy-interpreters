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

    def parse(self) -> list["ast.statements.Statement"]:
        stmts: list["ast.statements.Statement"] = []

        while not self.is_at_end():
            declaration = self.declaration()
            if declaration:
                stmts.append(declaration)

        return stmts

    """
    Statements
    """

    def declaration(self) -> "ast.statements.Statement | None":
        try:
            if self.match([TokenType.VAR]):
                return self.variable_declaration()

            return self.statement()
        except ParseError:
            self.synchronise()
            return None

    def variable_declaration(self) -> "ast.statements.Var":
        name: Token = self.consume(TokenType.IDENTIFIER, "Expected variable name.")

        initialiser = None
        if self.match([TokenType.EQUAL]):
            initialiser = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected assignment to end with ';'.")
        return ast.statements.Var(name, initialiser)

    def statement(self) -> "ast.statements.Statement":
        if self.match([TokenType.PRINT]):
            return self.print_statement()

        if self.match([TokenType.LEFT_BRACE]):
            return self.block()

        return self.expression_statement()

    def print_statement(self) -> "ast.statements.Print":
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return ast.statements.Print(expr)

    def block(self) -> "ast.statements.Block":
        statements = []

        while not (self.check(TokenType.RIGHT_BRACE) or self.is_at_end()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expected closing '}'.")

        return ast.statements.Block(statements)

    def expression_statement(self) -> "ast.statements.Expression":
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression.")

        return ast.statements.Expression(expr)

    """
    Expressions
    """

    def expression(self) -> "ast.expressions.Expression":
        return self.assignment()

    def assignment(self) -> "ast.expressions.Expression":
        expr = self.equality()

        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, ast.expressions.Variable):
                name = expr.name
                return ast.expressions.Assignment(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def equality(self) -> "ast.expressions.Expression":
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.equality()

            expr = ast.expressions.Binary(expr, operator, right)

        return expr

    def comparison(self) -> "ast.expressions.Expression":
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

            expr = ast.expressions.Binary(expr, operator, right)

        return expr

    def term(self) -> "ast.expressions.Expression":
        expr = self.factor()

        while self.match([TokenType.PLUS, TokenType.MINUS]):
            operator = self.previous()
            right = self.factor()

            expr = ast.expressions.Binary(expr, operator, right)

        return expr

    def factor(self) -> "ast.expressions.Expression":
        expr = self.unary()

        while self.match([TokenType.STAR, TokenType.SLASH]):
            operator = self.previous()
            right = self.unary()

            expr = ast.expressions.Binary(expr, operator, right)

        return expr

    def unary(self) -> "ast.expressions.Expression":
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return ast.expressions.Unary(operator, right)

        return self.primary()

    def primary(self) -> "ast.expressions.Expression":
        if self.match([TokenType.TRUE]):
            return ast.expressions.Literal(True)
        elif self.match([TokenType.FALSE]):
            return ast.expressions.Literal(False)
        elif self.match([TokenType.NIL]):
            return ast.expressions.Literal(None)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return ast.expressions.Literal(self.previous().literal)

        if self.match([TokenType.IDENTIFIER]):
            return ast.expressions.Variable(self.previous())

        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return ast.expressions.Grouping(expr)

        raise self.error(self.peek(), "Expected expression.")

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
        return self.peek().type == TokenType.EOF

    def peek(self) -> "Token":
        return self.tokens[self.current]

    def previous(self) -> "Token":
        return self.tokens[self.current - 1]

    def consume(self, expected: "TokenType", message: str) -> "Token":
        if self.check(expected):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token: "Token", message: str) -> "ParseError":
        from lox import Lox

        error = ParseError(token, message)
        Lox.parse_error(error)

        return error

    def synchronise(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return

            self.advance()
