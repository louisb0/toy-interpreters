from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lox.lexer import Token

from lox.lexer import Lexer
from lox.parser import Parser, ParseError
from lox.interpreter import Interpreter, RuntimeError


class Lox:
    had_parse_error: bool = False
    had_runtime_error: bool = False

    @staticmethod
    def run_program(source: str):
        lexer = Lexer(source)
        tokens: list["Token"] = lexer.read_tokens()

        parser = Parser(tokens)
        program = parser.parse()

        if Lox.had_parse_error or not program:
            return

        Interpreter().interpret(program)

    @staticmethod
    def start_repl():
        while True:
            try:
                print("> ", end="")

                Lox.run_program(input())
                Lox.had_parse_error = False
                Lox.had_runtime_error = False
            except (KeyboardInterrupt, EOFError):
                print()
                break

    @staticmethod
    def parse_error(error: ParseError):
        where = "end of file" if error.is_eof else f"'{error.token.raw}'"

        print(f"[line {error.token.line}] ParseError at {where}: {str(error)}")
        Lox.had_parse_error = True

    @staticmethod
    def runtime_error(error: RuntimeError):
        print(f"[line {error.token.line}] RuntimeError: {str(error)}")
        Lox.had_runtime_error = True
