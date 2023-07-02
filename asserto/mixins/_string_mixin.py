from typing_extensions import Self

from ._protocols import Assertable


class AssertsStringsMixin(Assertable):
    """A Mixin class that composes functionality for asserting against strings.
    Some functionality is applicable to general Sequence types too."""

    def ends_with(self, suffix: str) -> Self:
        if not self.actual.endswith(suffix):
            raise AssertionError(f"{self.actual} did not end with {suffix=}")
        return self
