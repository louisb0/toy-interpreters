from src.lexer import Lexer
from src.parser import Parser
from src.token import Token

PROMPT = ">> "


def main():
    expression = input(PROMPT)

    while expression:
        lexer = Lexer(expression)
        parser = Parser(lexer)

        print(parser.parse_program())

        expression = input(PROMPT)


if __name__ == "__main__":
    main()
