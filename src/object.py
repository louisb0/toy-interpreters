from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


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
    def __init__(self, value: Object | None):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
