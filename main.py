from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import Evaluator
import src.ast as ast

PROMPT = ">> "


def main():
    print("=" * 60)
    print("Prefix your expression with 'visualise: ' to get a rendered AST.")
    print("=" * 60)

    while True:
        expression = input(PROMPT)
        if not expression:
            return

        visualise_ast = "visualise: " in expression.lower()
        expression = expression.replace("visualise: ", "")

        lexer = Lexer(expression)
        parser = Parser(lexer)
        program = parser.parse_program()

        if len(parser.errors) != 0:
            print("\n".join(parser.errors))
            continue

        if visualise_ast:
            graph = ast.ast_to_dot(program)
            graph.render("ast", format="png", view=True)

        evaluated = Evaluator.eval(program)
        print(evaluated)

if __name__ == "__main__":
    main()
