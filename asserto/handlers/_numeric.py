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
            raise AssertionError(f"{self.actual} was not equal to `0`.")
