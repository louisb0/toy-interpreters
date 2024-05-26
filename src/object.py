from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


class Environment:
    def __init__(self):
        self.store: dict[str, Object] = {}

    def get(self, name: str) -> Object | None:
        return self.store.get(name)

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
