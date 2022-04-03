from __future__ import annotations

__tracebackhide__ = True


class StringMixin:
    def ends_with(self, suffix: str) -> StringMixin:
        if not self.value.endswith(suffix):
            self.error(f"{self.value} did not end with {suffix}")

    def starts_with(self, prefix: str) -> StringMixin:
        if not self.value.startswith(prefix):
            self.error(f"{self.value} did not end with {prefix}")
