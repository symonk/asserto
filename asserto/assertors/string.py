from __future__ import annotations

__tracebackhide__ = True

from .._mixins import AsserterMixin


class AssertsStrings(AsserterMixin):
    def __init__(self, value: str) -> None:
        self.value = value

    def ends_with(self, suffix: str) -> None:
        if not self.value.endswith(suffix):
            self.error(f"{self.value} did not end with {suffix}")

    def starts_with(self, prefix: str) -> None:
        if not self.value.startswith(prefix):
            self.error(f"{self.value} did not end with {prefix}")
