from abc import ABC, abstractmethod
import src.ast as ast


class Object(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


class Environment:
    def __init__(self, outer: "Environment | None" = None):
        self.store: dict[str, Object] = {}

        self.outer = outer

    def get(self, name: str) -> Object | None:
        result = self.store.get(name)

        if not result and self.outer is not None:
            return self.outer.get(name)

        return result

    def set(self, name: str, value: Object):
        self.store[name] = value


class Integer(Object):
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Boolean(Object):
    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        return str(self.value).lower()


class Null(Object):
    def __str__(self) -> str:
        return "null"


class ReturnValue(Object):
    def __init__(self, value: Object):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Error(Object):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class Function(Object):
    def __init__(
        self,
        parameters: list[ast.Identifier],
        body: ast.BlockStatement,
        env: Environment,
    ):
        self.parameters = parameters
        self.body = body
        self.env = env

    def __str__(self):
        return f"""fn({', '.join(str(p) for p in self.parameters)}) {{
            {str(self.body)}
        }}"""
