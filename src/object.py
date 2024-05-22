from abc import ABC, abstractmethod


class ObjectTypes:
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"


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


class Boolean(Object):
    def __init__(self, value: bool):
        self.value = value

    def type(self) -> str:
        return ObjectTypes.BOOLEAN

    def __str__(self) -> str:
        return str(self.value).lower()


class Null(Object):
    def type(self) -> str:
        return ObjectTypes.NULL

    def __str__(self) -> str:
        return "null"
