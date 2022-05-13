import abc
import typing

from ._matchable import Matchable


class ValidatesRegexTypes(Matchable):
    def matches(self, actual: typing.Any) -> None:
        pass

    @abc.abstractmethod
    def matches_criteria(self, actual: typing.Any) -> None:
        """Todo: Implement properly"""
