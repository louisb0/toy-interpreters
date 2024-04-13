class Token:
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"
    INT = "INT"

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"

    KEYWORD_MAPPING = {
        "fn": FUNCTION,
        "let": LET,
        "true": TRUE,
        "false": FALSE,
        "if": IF,
        "else": ELSE,
        "return": RETURN,
    }

    def __init__(self, token_type: str, literal: str):
        self.token_type: str = token_type
        self.literal: str = literal

    @staticmethod
    def lookup_identifier(identifier: str):
        mapped_value = Token.KEYWORD_MAPPING.get(identifier)

        return mapped_value if mapped_value else Token.IDENT

    def __eq__(self, value: "Token"):
        print((self.literal, value.literal))
        return (self.token_type == value.token_type) and (self.literal == value.literal)

    def __str__(self):
        return f"{self.token_type} ({self.literal})"
