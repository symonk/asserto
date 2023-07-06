from typing import Any
from typing import Iterable

from typing_extensions import Self

from .._decorators import enforce_actual_has_type_of
from .._protocols import Assertable
from .._util import to_iterable

# Todo: end_with offering a `start` and `end`?
# Todo: starts_with offering a `start` and `end`?
# Todo: Docs reuse through __doc__ ?
# Todo: Utility functions and general DRY here
# Todo: This is our first mixin impl, so let's make it perfect before rolling out.


class AssertsStringsMixin(Assertable):
    """Mixin responsible for composing assertions for string types."""

    def ends_with(self, suffix: str) -> Self:
        """Asserts the actual value ends with a given prefix.  If the actual
        value is an iterable, the last element within it will be compared for
        equality (==) against the suffix.

        :param suffix: The expected substring for the actual value to end with.

        :raises TypeError: When the actual value is not a string or iterable.
        :raises TypeError: When the suffix value is not a string.
        :raises ValueError: When the suffix or actual values are empty.
        :raises ValueError: When the actual value is an empty string.
        :raises AssertionError: When the actual value does not end with the suffix.

        :return: The `Asserto` instance for fluent chaining.
        """
        if isinstance(self.actual, str):
            if not suffix:
                raise ValueError(f"{suffix=} must not be empty.")
            if not isinstance(suffix, str):
                raise TypeError(f"{suffix=} must be a string.")
            if not self.actual.endswith(suffix):
                self.error(f"Expected `{self.actual}` to end with {suffix=} but it did not.")
        elif isinstance(self.actual, Iterable):
            if not self.actual:
                raise ValueError(f"{self.actual} must not be empty.")

            last: Iterable[Any] = to_iterable(self.actual)[-1]
            if last != suffix:
                self.error(f"Expected `{self.actual}` to end with {suffix=} but it did not.")
        else:
            raise TypeError(f"{self.actual} is not a string or iterable.")
        return self

    @enforce_actual_has_type_of(str)
    def is_alpha(self) -> Self:
        """Asserts the actual value is considered alphabetic.  Empty strings will
        not be considered alphabetic for this case.

        :raises TypeError: If the actual value is not of type string.
        :raises AssertionError: If the actual value is not an alphabetic string.

        :return: The `Asserto` instance for fluent chaining.
        """
        if not self.actual.isalpha():
            self.error(f"{self.actual} is not alphabetic.")

        return self

    @enforce_actual_has_type_of(str)
    def is_digit(self) -> Self:
        """Asserts the actual value is a digit string.  Empty strings will not be considered
        digit strings for this case.

        :raises TypeError: If the actual value is not of type string.
        :raises AssertionError: If the actual value is not an alphabetic string.

        :return: The `Asserto` instance for fluent chaining.
        """
        if not self.actual.isdigit():
            self.error(f"{self.actual} is not a digit string.")
        return self

    def starts_with(self, prefix: str) -> Self:
        """Asserts the actual value starts with the prefix.  If the actual value is
        an iterable the first element is compared for equality (==) against the prefix.


        :param prefix: The value to check the actual value starts with.

        """
        if not isinstance(prefix, str):
            raise TypeError(f"starts_with prefix must be a string, not: {type(prefix)}")
        if not prefix:
            raise ValueError("starts_with cannot be called with an empty prefix string")

        if isinstance(self.actual, Iterable):
            if isinstance(self.actual, str):
                if not self.actual.startswith(prefix):
                    self.error(f"{self.actual} did not begin with {prefix=}")
            else:
                iterable = iter(self.actual)
                first = next(iterable, None)
                if first is None:
                    raise ValueError(f"cannot check if an empty iterable started with {prefix}")
                if first != prefix:
                    self.error(f"{self.actual} did not start with {prefix}")
        else:
            raise TypeError("starts_with cannot be called if the actual value is not a string or iterable")
        return self
