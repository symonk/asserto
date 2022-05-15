import re
import typing

from .._types import RE_FLAGS_ALIAS
from .._types import RE_PATTERN_ALIAS
from ..descriptors import IsInstanceOf


class RegexHandler:
    """
    Regular expression handler.
    """

    actual: typing.Any = IsInstanceOf(str, re.Pattern)

    def __init__(self, actual: typing.Any) -> None:
        self.actual = actual

    def match(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> bool:
        """Matches the beginning of a string"""
        if not re.match(pattern, self.actual, flags):
            raise AssertionError(f"{self.actual} did not begin with pattern: {pattern}")
        return re.match(pattern, self.actual, flags) is not None

    def search(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS) -> None:
        raise NotImplementedError

    def full_match(self, pattern: RE_PATTERN_ALIAS, count: int, flags: RE_FLAGS_ALIAS) -> None:
        raise NotImplementedError

    def findall(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS):
        raise NotImplementedError
