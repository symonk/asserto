import abc
import typing

from ._acceptable import Matchable


class ValidatesRegexTypes(Matchable):
    def matches(self, actual: typing.Any) -> None:
        pass

    @abc.abstractmethod
    def matches(self, *args, **kw):
        """Todo: Implement properly"""
