from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token

from lox.lexer import Lexer
from lox.parser import Parser
from lox.interpreter import Interpreter, RuntimeError


class Lox:
    had_error: bool = False
    had_runtime_error: bool = False

    @staticmethod
    def run_program(source: str):
        lexer = Lexer(source)
        tokens: list["Token"] = lexer.read_tokens()

        parser = Parser(tokens)
        program = parser.parse()

        if Lox.had_error or not program:
            return

        Interpreter().interpret(program)

    @staticmethod
    def start_repl():
        while True:
            try:
                print("> ", end="")

                Lox.run_program(input())
                Lox.had_error = False
                Lox.had_runtime_error = False
            except (KeyboardInterrupt, EOFError):
                print()
                break

    @staticmethod
    def error(line: int, message: str, where: str = ""):
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True

    @staticmethod
    def runtime_error(error: RuntimeError):
        print(f"[line {error.token.line}] {str(error)}")
        Lox.had_error = True
