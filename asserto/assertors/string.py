from __future__ import annotations

__tracebackhide__ = True

from .._mixins import AsserterMixin


class AssertsStrings(AsserterMixin):
    def __init__(self, actual: str) -> None:
        self.actual = actual

    def ends_with(self, suffix: str) -> None:
        if not self.actual.endswith(suffix):
            self.error(f"{self.actual} did not end with {suffix}")

    def starts_with(self, prefix: str) -> None:
        if not self.actual.startswith(prefix):
            self.error(f"{self.actual} did not end with {prefix}")
