import typing

from ..descriptors import ValidatesInstanceOf
from ._handler import Handler


class StringHandler(Handler):
    """
    A handler responsible for all string based checks.
    """

    actual: str = ValidatesInstanceOf(str)  # type: ignore[assignment]

    def __init__(self, actual: typing.Any) -> None:
        super().__init__(actual)

    def is_alpha(self) -> None:
        if self.raise_if_length_equals() and not self.actual.isalpha():
            raise AssertionError(f"{self.actual} did not contain only alpha numeric characters.")

    def is_digit(self) -> None:
        if self.raise_if_length_equals() and not self.actual.isdigit():
            raise AssertionError(f"{self.actual} did not contain only numeric digits.")

    def ends_with(self, suffix: str) -> None:
        if not self.actual.endswith(suffix):
            raise AssertionError(f"{self.actual} did not end with {suffix=}")

    def starts_with(self, prefix: str) -> None:
        if not self.actual.startswith(prefix):
            raise AssertionError(f"{self.actual} did not begin with {prefix=}")
