import abc
import typing


class Matchable:
    """
    Interface for type handlers to verify if they can accept
    the target value or not.  Handlers which cannot accept
    the type should raise a `ValueError` otherwise return
    nothing.
    """

    @abc.abstractmethod
    def matches_criteria(self, actual: typing.Any) -> None:
        raise NotImplementedError
