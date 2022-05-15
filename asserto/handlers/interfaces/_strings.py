import abc

from ._checkable import AcceptsType


class ValidateString(AcceptsType):
    @abc.abstractmethod
    def ends_with(self, suffix: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def starts_with(self, prefix: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def is_digit(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def is_alpha(self) -> bool:
        raise NotImplementedError
