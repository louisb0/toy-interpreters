from src.lexer import Lexer
from src.parser import Parser
import src.ast as ast

PROMPT = ">> "


def main():
    print("=" * 60)
    print("Prefix your expression with 'visualise: ' to get a rendered AST.")
    print("=" * 60)

    expression = input(PROMPT)
    while expression:
        visualise_ast = "visualise: " in expression.lower()

        lexer = Lexer(expression)
        parser = Parser(lexer)
        program = parser.parse_program()

        if len(parser.errors) != 0:
            print("\n".join(parser.errors))
        else:
            print(program)
            if visualise_ast:
                graph = ast.ast_to_dot(program)
                graph.render("ast", format="png", view=True)

        expression = input(PROMPT)


if __name__ == "__main__":
    main()
