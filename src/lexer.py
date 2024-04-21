from src.token import Token


class Lexer:
    def __init__(self, program: str):
        self.program: str = program

        self.position: int = 0
        self.read_position: int = 0
        self.char: str = None

        self._read_char()

    def next_token(self):
        token: Token = None

        self._skip_whitespace()

        match self.char:
            case "=":
                if self._peak_char() == "=":
                    old_char = self.char
                    self._read_char()

                    token = Token(Token.EQ, old_char + self.char)
                else:
                    token = Token(Token.ASSIGN, self.char)
            case ";":
                token = Token(Token.SEMICOLON, self.char)
            case ",":
                token = Token(Token.COMMA, self.char)
            case "(":
                token = Token(Token.LPAREN, self.char)
            case ")":
                token = Token(Token.RPAREN, self.char)
            case "{":
                token = Token(Token.LBRACE, self.char)
            case "}":
                token = Token(Token.RBRACE, self.char)
            case "+":
                token = Token(Token.PLUS, self.char)
            case "-":
                token = Token(Token.MINUS, self.char)
            case "!":
                if self._peak_char() == "=":
                    old_char = self.char
                    self._read_char()

                    token = Token(Token.NOT_EQ, old_char + self.char)
                else:
                    token = Token(Token.BANG, self.char)
            case "*":
                token = Token(Token.ASTERISK, self.char)
            case "/":
                token = Token(Token.SLASH, self.char)
            case "<":
                token = Token(Token.LT, self.char)
            case ">":
                token = Token(Token.GT, self.char)
            case _:
                if self.char.isalpha():
                    literal = self._read_identifier()
                    token_type = Token.lookup_identifier(literal)

                    return Token(token_type, literal)
                elif self.char.isnumeric():
                    literal = self._read_number()

                    return Token(Token.INT, literal)
                elif self.char == "":
                    token = Token(Token.EOF, self.char)
                else:
                    token = Token(Token.ILLEGAL, self.char)

        self._read_char()
        return token

    def _read_char(self) -> str:
        if self.read_position >= len(self.program):
            self.char = ""
        else:
            self.char = self.program[self.read_position]

        self.position = self.read_position
        self.read_position += 1

    def _read_identifier(self) -> str:
        starting_position = self.position

        while self.char.isalpha() or self.char == "_":
            self._read_char()

        return self.program[starting_position : self.position]

    def _read_number(self) -> int:
        starting_position = self.position

        while self.char.isnumeric():
            self._read_char()

        return self.program[starting_position : self.position]

    def _peak_char(self) -> str:
        if self.read_position >= len(self.program):
            return ""
        else:
            return self.program[self.read_position]

    def _skip_whitespace(self) -> None:
        while (
            self.char == " "
            or self.char == "\n"
            or self.char == "\t"
            or self.char == "\r"
        ):
            self._read_char()
