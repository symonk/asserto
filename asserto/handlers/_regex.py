import re
import typing

from ..descriptors import IsInstanceOf
from .interfaces import ValidateRegex


class RegexHandler(ValidateRegex):
    """
    Regular expression handler.
    """

    actual: typing.Any = IsInstanceOf(str, re.Pattern)

    def __init__(self, actual: typing.Any) -> None:
        self.actual = actual

    def matches_beginning(self, expected: typing.Any, flags: typing.Union[int, re.RegexFlag] = 0) -> bool:
        """Matches the beginning of a string"""
        return re.match(expected, self.actual, flags) is not None

    def contains_match(self, expected: typing.Any, flags: typing.Union[int, re.RegexFlag] = 0) -> bool:
        ...
