import numbers

from ..descriptors import EnforcedInstanceOf
from ._base import Handler


class NumericHandler(Handler):
    """A Handler for all things numeric."""

    actual: EnforcedInstanceOf[numbers.Number] = EnforcedInstanceOf(numbers.Number)

    def __init__(self, actual: numbers.Number) -> None:
        super().__init__(actual)

    def is_zero(self) -> None:
        """Checks if a numeric type is explicitly zero"""
        if self.actual != 0:
            raise AssertionError(f"{self.actual} was not equal to 0")

    def is_not_zero(self) -> None:
        """Checks if a numeric type is not zero"""
        if self.actual == 0:
            raise AssertionError(f"{self.actual} was 0")

    def is_greater_than(self, target: numbers.Number) -> None:
        """Checks if a number is greater than a value"""
        if self.actual <= target:
            raise AssertionError(f"{self.actual} was less than {target}")
