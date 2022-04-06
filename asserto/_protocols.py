import abc
import typing


class Assertable(typing.Protocol):
    @abc.abstractmethod
    def error(self, reason: str) -> typing.NoReturn:
        raise NotImplementedError
