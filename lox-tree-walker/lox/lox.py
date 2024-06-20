from lox.lexer import Lexer, Token
from lox.parser import Parser
from lox.visitors import TreePrinter


class Lox:
    had_error: bool = False

    @staticmethod
    def run_program(source: str):
        lexer = Lexer(source)
        tokens: list[Token] = lexer.read_tokens()

        parser = Parser(tokens)
        program = parser.parse()

        if Lox.had_error:
            return
        
        print(program.accept(TreePrinter()))

    @staticmethod
    def start_repl():
        while True:
            try:
                print("> ", end="")

                Lox.run_program(input())
                Lox.had_error = False
            except (KeyboardInterrupt, EOFError):
                print()
                break

    @staticmethod
    def error(line: int, message: str, where: str = ""):
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True
