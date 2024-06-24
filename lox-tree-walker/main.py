import sys

from lox import Lox


def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py [script]")
    elif len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            Lox.run_program(f.read())
            if Lox.had_error:
                sys.exit(1)
            elif Lox.had_runtime_error:
                sys.exit(2)
    else:
        Lox.start_repl()


if __name__ == "__main__":
    main()
