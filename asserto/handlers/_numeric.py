from ._base import Handler


class NumberHandler(Handler):
    """A Handler for handling numeric types of data.  Non instances of
    pythons float will be failed instantly by the descriptor,
    so it is safe to assume that all methods here are acting on a stored
    actual value that is in fact, numeric.

    Asserto is catching AssertionError's raised from this handler and shaping
    its own with the exception message provided.
    """

    def __init__(self, actual: float) -> None:
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

    def is_greater_than(self, other: float) -> None:
        """Asserts that the value is numeric, and it is lesser than other"""
        if self.actual <= other:
            raise AssertionError(f"Expected {self.actual} to be greater than {other}, but it was not.")

    def is_lesser_than(self, other: float) -> None:
        """Asserts that the value is a numeric type and is lesser than other"""
        if self.actual >= other:
            raise AssertionError(f"Expected {self.actual} to be lesser than {other}, but it was not.")

    def is_positive(self) -> None:
        """Asserts that the value is numeric, and is greater than 0"""
        return self.is_greater_than(0)  # type: ignore[arg-type]

    def is_negative(self) -> None:
        """Asserts that the value is numeric, and is lesser than 0"""
        return self.is_lesser_than(0)  # type: ignore[arg-type]

    def is_between(self, low: float, high: float, inclusive: bool = False):
        """Asserts tht the value is numeric and is between lower and higher.  If inclusive
        is true, value is considered between if it equals either the lower or higher bounds.
        """
        if inclusive:
            low -= 1
            high += 1
        if self.actual <= low or self.actual >= high:
            raise AssertionError(f"Expected {self.actual} to be between ({low}, ..., {high})")

    def is_not_between(self, low: float, high: float, inclusive: bool = False):
        """Asserts that the value is numeric and is not between a low and high bounds.  If inclusive
        is true, value is considered between if it equals either the low or high bounds."""
        try:
            return self.is_between(low, high, inclusive)
        except AssertionError:
            ...
        raise AssertionError(f"Expected {self.actual} to not be between ({low}, ..., {high})")

    def _validate_number(self) -> None:
        if isinstance(self.actual, float) is False or isinstance(self.actual, bool) is True:
            raise ValueError()
