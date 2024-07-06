from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import lox.ast as ast
    from lox.lexer import Token
    from lox.errors import ParseError, RuntimeError


class Lox:
    from lox.interpreter import Interpreter

    had_parse_error: bool = False
    had_runtime_error: bool = False

    _interpreter = Interpreter()

    @staticmethod
    def run_program(source: str):
        from lox.lexer import Lexer
        from lox.parser import Parser
        from lox.resolver import Resolver

        lexer = Lexer(source)
        tokens: list["Token"] = lexer.read_tokens()

        parser = Parser(tokens)
        program: list["ast.statements.Statement"] = parser.parse()

        if Lox.had_parse_error:
            return

        resolver = Resolver(Lox._interpreter)
        resolver.resolve_statements(program)

        if Lox.had_parse_error:
            return

        Lox._interpreter.interpret(program)

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
    def parse_error(error: "ParseError"):
        where = "end of file" if error.is_eof else f"'{error.token.raw}'"

        print(f"[line {error.token.line}] ParseError at {where}: {str(error)}")
        Lox.had_parse_error = True

    @staticmethod
    def runtime_error(error: "RuntimeError"):
        print(f"[line {error.token.line}] RuntimeError: {str(error)}")
        Lox.had_runtime_error = True
