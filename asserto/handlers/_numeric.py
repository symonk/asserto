import numbers
import operator

from ._base import Handler


class NumberHandler(Handler):
    """A Handler for handling numeric types of data.  Non instances of
    pythons numbers.Number will be failed instantly by the descriptor,
    so it is safe to assume that all methods here are acting on a stored
    actual value that is in fact, numeric.

    Asserto is catching AssertionError's raised from this handler and shaping
    its own with the exception message provided.
    """

    def __init__(self, actual: numbers.Number) -> None:
        super().__init__(actual)
        self._validate_number()

    def is_zero(self) -> None:
        """Asserts that the value is a numeric type and is equal to 0"""
        if self.actual != 0:
            raise AssertionError(f"Expected {self.actual} to be 0 but it was not.")

    def is_not_zero(self) -> None:
        """Asserts that the value is numeric, and it is greater than other"""
        if self.actual == 0:
            raise AssertionError(f"Expected {self.actual} to not be 0 but it was.")

    def is_greater_than(self, other: numbers.Number) -> None:
        """Asserts that the value is numeric, and it is lesser than other"""
        if self.actual <= other:
            raise AssertionError(f"Expected {self.actual} to be greater than {other}, but it was not.")

    def is_lesser_than(self, other: numbers.Number) -> None:
        """Asserts that the value is a numeric type and is lesser than other"""
        if self.actual >= other:
            raise AssertionError(f"Expected {self.actual} to be lesser than {other}, but it was not.")

    def is_positive(self) -> None:
        """Asserts that the value is numeric, and is greater than 0"""
        return self.is_greater_than(0)  # type: ignore[arg-type]

    def is_negative(self) -> None:
        """Asserts that the value is numeric, and is lesser than 0"""
        return self.is_lesser_than(0)  # type: ignore[arg-type]

    def is_between(self, low: numbers.Number, high: numbers.Number, inclusive: bool = False):
        """Asserts tht the value is numeric and is between lower and higher.  If inclusive
        is true, value is considered between if it equals either the lower or higher bounds.
        """
        low_fn, high_fn = (operator.lt, operator.gt) if not inclusive else (operator.le, operator.ge)
        return low_fn(self.actual, low) and high_fn(self.actual, high)

    def is_not_between(self, low: numbers.Number, high: numbers.Number, inclusive: bool = False):
        """Asserts that the value is numeric and is not between a low and high bounds.  If inclusive
        is true, value is considered between if it equals either the low or high bounds."""
        return not self.is_between(low, high, inclusive)

    def _validate_number(self) -> None:
        if isinstance(self.actual, numbers.Number) is False or isinstance(self.actual, bool) is True:
            raise ValueError()
