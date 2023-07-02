from ._protocols import Assertable
from typing import TypeVar


AssertoSelfType = TypeVar("AssertoSelfType", bound=Assertable)

class AssertsStringsMixin(Assertable):
    """A Mixin class that composes functionality for asserting against strings.
    Some functionality is applicable to general Sequence types too."""

    def ends_with(self: AssertoSelfType, suffix: str) -> AssertoSelfType:
        if not self.actual.endswith(suffix):
            raise AssertionError(f"{self.actual} did not end with {suffix=}")
        return self

