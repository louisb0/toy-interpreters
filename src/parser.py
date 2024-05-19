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
        self._register_prefix(Token.BANG, self._parse_prefix_expression)
        self._register_prefix(Token.MINUS, self._parse_prefix_expression)
        self._register_prefix(Token.TRUE, self._parse_boolean)
        self._register_prefix(Token.FALSE, self._parse_boolean)
        self._register_prefix(Token.LPAREN, self._parse_grouped_expression)
        self._register_prefix(Token.IF, self._parse_if_expression)
        self._register_prefix(Token.FUNCTION, self._parse_function_literal)

        self.infix_parse_functions: dict = {}
        self._register_infix(Token.PLUS, self._parse_infix_expression)
        self._register_infix(Token.MINUS, self._parse_infix_expression)
        self._register_infix(Token.SLASH, self._parse_infix_expression)
        self._register_infix(Token.ASTERISK, self._parse_infix_expression)
        self._register_infix(Token.EQ, self._parse_infix_expression)
        self._register_infix(Token.NOT_EQ, self._parse_infix_expression)
        self._register_infix(Token.LT, self._parse_infix_expression)
        self._register_infix(Token.GT, self._parse_infix_expression)
        self._register_infix(Token.LPAREN, self._parse_call_expression)

        self.precedences: dict[str, Precedence] = {
            Token.EQ: Precedence.EQUALS,
            Token.NOT_EQ: Precedence.EQUALS,
            Token.LT: Precedence.LESSGREATER,
            Token.GT: Precedence.LESSGREATER,
            Token.PLUS: Precedence.SUM,
            Token.MINUS: Precedence.SUM,
            Token.SLASH: Precedence.PRODUCT,
            Token.ASTERISK: Precedence.PRODUCT,
            Token.LPAREN: Precedence.CALL,
        }

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
        prefix = self.prefix_parse_functions.get(self.current_token.token_type)
        if prefix is None:
            self.errors.append(
                f"no prefix parse function for {self.current_token.token_type} found"
            )
            return None

        left_expression = prefix()

        while (
            self.peak_token.token_type != Token.SEMICOLON
            and precedence.value
            < self.precedences.get(self.peak_token.token_type, Precedence.LOWEST).value
        ):
            infix = self.infix_parse_functions.get(self.peak_token.token_type)
            if infix == None:
                return left_expression

            self._next_token()
            left_expression = infix(left_expression)

        return left_expression

    def _parse_prefix_expression(self) -> ast.Expression:
        expression = ast.PrefixExpression(
            self.current_token, self.current_token.literal
        )

        self._next_token()

        expression.right = self._parse_expression(Precedence.PREFIX)
        return expression

    def _parse_infix_expression(self, left: ast.Expression) -> ast.Expression | None:
        expression = ast.InfixExpression(
            self.current_token, self.current_token.literal, left
        )

        precedence = self.precedences.get(
            self.current_token.token_type, Precedence.LOWEST
        )
        self._next_token()
        expression.right = self._parse_expression(precedence)

        return expression

    def _parse_grouped_expression(self):
        self._next_token()

        expression = self._parse_expression(Precedence.LOWEST)
        if not self._expect_peek(Token.RPAREN):
            return None

        return expression

    def _parse_if_expression(self):
        expression = ast.IfExpression(self.current_token)

        if not self._expect_peek(self.current_token.LPAREN):
            return None

        self._next_token()

        expression.condition = self._parse_expression(Precedence.LOWEST)

        if not self._expect_peek(Token.RPAREN):
            return None
        if not self._expect_peek(Token.LBRACE):
            return None

        expression.consequence = self._parse_block_statement()

        if self.peak_token.token_type == Token.ELSE:
            self._next_token()

            if not self._expect_peek(Token.LBRACE):
                return None

            expression.alternative = self._parse_block_statement()

        return expression

    def _parse_block_statement(self):
        block = ast.BlockStatement(self.current_token)
        self._next_token()

        while (
            self.current_token.token_type != Token.RBRACE
            and self.current_token.token_type != Token.EOF
        ):
            statement = self._parse_statement()
            if statement != None:
                block.statements.append(statement)
            self._next_token()

        return block

    def _parse_function_literal(self):
        function = ast.FunctionLiteral(self.current_token)

        if not self._expect_peek(Token.LPAREN):
            return None

        function.parameters = self._parse_parameters()

        if not self._expect_peek(Token.LBRACE):
            return None

        function.body = self._parse_block_statement()

        return function

    def _parse_parameters(self) -> list[ast.Identifier]:
        identifiers: list[ast.Identifier] = []

        if self.peak_token.token_type == Token.RPAREN:
            self._next_token()
            return identifiers

        self._next_token()
        identifiers.append(self._parse_identifier())

        while self.peak_token.token_type == Token.COMMA:
            self._next_token()
            self._next_token()

            identifiers.append(self._parse_identifier())

        if not self._expect_peek(Token.RPAREN):
            return None

        return identifiers

    def _parse_call_expression(self, expression: ast.Identifier | ast.FunctionLiteral):
        call = ast.CallExpression(self.current_token, expression)
        call.arguments = self._parse_call_arguments()

        return call

    def _parse_call_arguments(self):
        args: list[ast.Expression] = []

        if self.peak_token.token_type == Token.RPAREN:
            self._next_token()
            return args

        self._next_token()
        args.append(self._parse_expression(Precedence.LOWEST))

        while self.peak_token.token_type == Token.COMMA:
            self._next_token()
            self._next_token()

            args.append(self._parse_expression(Precedence.LOWEST))

        if not self._expect_peek(Token.RPAREN):
            return None

        return args

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

    def _parse_boolean(self) -> ast.Expression:
        return ast.Boolean(
            self.current_token, self.current_token.token_type == Token.TRUE
        )

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
