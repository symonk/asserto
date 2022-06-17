import re
import typing

from .._types import RE_FLAGS_ALIAS
from .._types import RE_PATTERN_ALIAS
from ..descriptors import ValidatesInstanceOf
from ._handler import Handler


class RegexHandler(Handler):
    """
    Regular expression handler.
    """

    actual: typing.Any = ValidatesInstanceOf(str, re.Pattern)

    def __init__(self, actual: typing.Any) -> None:
        super().__init__(actual)

    def match(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> None:
        """Matches the beginning of a string"""
        if not re.match(pattern, self.actual, flags):
            raise AssertionError(f"{self.actual} did not begin with pattern: {pattern=}")

    def does_not_match(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> None:
        try:
            self.match(pattern, flags)
            raise AssertionError(f"{self.actual} was a match with pattern: {pattern=}")
        except AssertionError:
            pass

    def search(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS) -> None:
        if re.search(pattern, self.actual, flags) is None:
            raise AssertionError(f"{self.actual} did not contain any matches for: {pattern=}")

    def fullmatch(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS) -> None:
        if re.fullmatch(pattern, self.actual, flags) is None:
            raise AssertionError(f"{self.actual} was not matched entirely by: {pattern=}")

    def findall(self, pattern: RE_PATTERN_ALIAS, count: int, flags: RE_FLAGS_ALIAS) -> None:
        matches = re.findall(pattern, self.actual, flags)
        if len(matches) != count:
            raise AssertionError(
                f"{self.actual} had: {len(matches)} non overlapping occurrences for pattern: {pattern}, not: {count}"
            )
