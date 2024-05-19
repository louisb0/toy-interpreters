from src.lexer import Lexer
from src.parser import Parser

PROMPT = ">> "


def main():
    expression = input(PROMPT)

    while expression:
        lexer = Lexer(expression)
        parser = Parser(lexer)
        program = parser.parse_program()

        if len(parser.errors) == 0:
            print(program)
        else:
            print("\n".join(parser.errors))

        expression = input(PROMPT)


if __name__ == "__main__":
    main()
