import typing

from ..descriptors import IsInstanceOf
from .interfaces import ValidateString


class StringHandler(ValidateString):
    """
    A handler responsible for all string based checks.
    """

    actual: str = IsInstanceOf(str)

    def __init__(self, actual: typing.Any) -> None:
        self.actual = actual

    def is_alpha(self) -> bool:
        return self.actual.isalpha()

    def is_digit(self) -> bool:
        return self.actual.isdigit()

    def ends_with(self, suffix: str) -> bool:
        return self.actual.endswith(suffix)

    def starts_with(self, prefix: str) -> bool:
        return self.actual.startswith(prefix)
