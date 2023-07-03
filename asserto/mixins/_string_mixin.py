from typing import Any
from typing import Iterable

from typing_extensions import Self

from .._util import to_iterable
from ._protocols import Assertable


class AssertsStringsMixin(Assertable):
    """Mixin responsible for composing assertions for string types."""

    def ends_with(self, suffix: str) -> Self:
        """Asserts the actual value ends with the particular suffix.
        When the actual value is a string it is compared using the
        string builtin.  When the actual value is an iterable, the last
        element in the iterable is compared for equality against suffix.

        :param suffix: The expected substring for the actual value to end with.
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
