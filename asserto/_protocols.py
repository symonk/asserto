import abc
import typing


class Assertable(typing.Protocol):
    @abc.abstractmethod
    def error(self, reason: str) -> typing.NoReturn:
        raise NotImplementedError


class Reasonable(typing.Protocol):
    @abc.abstractmethod
    def format(self, reason: str) -> str:
        raise NotImplementedError
