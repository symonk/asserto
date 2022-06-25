import typing

from ._handler import Handler


class BaseHandler(Handler):
    """
    A handler for all objects.
    """

    def __init__(self, actual: typing.Any) -> None:
        super().__init__(actual)

    def is_true(self) -> None:
        """
        Asserts the actual value is explicitly True.
        """
        if not self.actual:
            raise AssertionError(f"{self.actual} was not True")

    def is_truthy(self) -> None:
        """
        Asserts the actual value is True in a boolean context.
        """
        if not bool(self.actual):
            raise AssertionError(f"{self.actual} was not truthy")

    def is_false(self) -> None:
        """
        Asserts the actual value is explicitly False.
        """
        if self.actual:
            raise AssertionError(f"{self.actual} was not False")

    def is_falsy(self) -> None:
        """
        Asserts the actual value is False in a boolean context.
        """
        if bool(self.actual):
            raise AssertionError(f"{self.actual} was not falsy")

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

    def is_instance(self, *other: typing.Any) -> None:
        if not isinstance(self.actual, other):
            raise AssertionError(f"{self.actual} was not an instance of: {other}")

    def has_same_identity_as(self, other: typing.Any) -> None:
        if self.actual is not other:
            raise AssertionError(f"{self.actual} does not share identity with: {other}")

    def does_not_have_same_identity_as(self, other: typing.Any) -> None:
        if self.actual is other:
            raise AssertionError(f"{self.actual} shares identity with: {other}")

    def is_none(self) -> None:
        if self.actual is not None:
            raise AssertionError(f"{self.actual} is not None")

    def is_not_none(self) -> None:
        if self.actual is None:
            raise AssertionError(f"{self.actual} is None")
