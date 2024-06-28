from enum import Enum, auto



class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()
    NONE = auto()

    @classmethod
    def from_keyword(cls, keyword):
        return {
            "and": cls.AND,
            "class": cls.CLASS,
            "else": cls.ELSE,
            "false": cls.FALSE,
            "for": cls.FOR,
            "fun": cls.FUN,
            "if": cls.IF,
            "nil": cls.NIL,
            "or": cls.OR,
            "print": cls.PRINT,
            "return": cls.RETURN,
            "super": cls.SUPER,
            "this": cls.THIS,
            "true": cls.TRUE,
            "var": cls.VAR,
            "while": cls.WHILE,
        }.get(keyword, None)


class Token:
    def __init__(self, type: TokenType, raw: str, line: int, literal=None):
        self.type = type
        self.raw = raw
        self.line = line
        self.literal = literal

    def __str__(self) -> str:
        return f"{str(self.type)}(raw='{self.raw}', line={self.line}, literal={self.literal})"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []

        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def read_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.read_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def read_token(self) -> None:
        char = self.advance()

        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case "*":
                self.add_token(TokenType.STAR)

            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )

            case '"':
                self.string()
            case _ if char.isdigit():
                self.number()
            case _ if char.isalpha():
                self.identifier()

            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            case _:
                from lox import Lox
                from lox.errors import ParseError

                # hack, needs cleanup
                Lox.parse_error(
                    ParseError(
                        Token(TokenType.NONE, char, self.line), "Unexpected character."
                    )
                )

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1

            self.advance()

        if self.is_at_end():
            from lox import Lox
            from lox.errors import ParseError

            # hack, needs cleanup
            Lox.parse_error(
                ParseError(
                    Token(TokenType.EOF, "", self.line), "Unclosed string literal."
                )
            )
            return

        # Closing '"'
        self.advance()

        # Trim surrounding '"'
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalpha():
            self.advance()

        text = self.source[self.start : self.current]
        type = TokenType.from_keyword(text)
        if type == None:
            type = TokenType.IDENTIFIER

        self.add_token(type)

    def advance(self) -> str:
        new_char = self.source[self.current]
        self.current += 1

        return new_char

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"

        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"

        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def add_token(self, type: TokenType, literal=None) -> None:
        raw = self.source[self.start : self.current]

        self.tokens.append(Token(type, raw, self.line, literal))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
