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
        program = parser.expression()

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
    def error(line: int, message: str):
        Lox._report(line, "", message)

    @staticmethod
    def _report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True
