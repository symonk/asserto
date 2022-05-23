import typing

from ._handler import Handler


class BaseHandler(Handler):
    """
    A handler for all objects.
    """

    def __init__(self, actual: typing.Any) -> None:
        super().__init__(actual)

    def is_true(self) -> None:
        if self.actual is False:
            raise AssertionError(f"{self.actual} was not True")

    def is_false(self) -> None:
        if self.actual is True:
            raise AssertionError(f"{self.actual} was not False")

    def is_equal_to(self, other: typing.Any) -> None:
        if self.actual != other:
            raise AssertionError(f"{self.actual} is not equal to: {other}")

    def is_not_equal_to(self, other: typing.Any) -> None:
        if self.actual == other:
            raise AssertionError(f"{self.actual} was equal to: {other}")

    def has_length(self, expected: int) -> None:
        if not isinstance(expected, int) or expected < 0:
            raise ValueError(f"{expected} must be an int and greater than 0")

        if len(self.actual) != expected:
            raise AssertionError(f"Length of: {self.actual!r} was not equal to: {expected!r}")
