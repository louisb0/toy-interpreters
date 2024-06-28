import time

from lox.objects import Callable

class NativeClock(Callable):
    def call(self, interpreter: "Interpreter", arguments: list):
        return time.time()

    def arity(self) -> int:
        return 0
