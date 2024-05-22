from abc import ABC, abstractmethod


class ObjectTypes:
    INTEGER = "INTEGER"


class Object(ABC):
    @abstractmethod
    def type(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()


class Integer(Object):
    def __init__(self, value: int):
        self.value = value

    def type(self) -> str:
        return ObjectTypes.INTEGER

    def __str__(self) -> str:
        return str(self.value)
