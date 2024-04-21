from src.lexer import Lexer
from src.token import Token

PROMPT = ">> "


def main():
    expression = input(PROMPT)

    while expression:
        lexer = Lexer(expression)

        for token in iter(lexer.next_token, Token(Token.EOF, "")):
            print(token)

        expression = input(PROMPT)


if __name__ == "__main__":
    main()
