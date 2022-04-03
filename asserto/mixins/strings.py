from __future__ import annotations

__tracebackhide__ = True


class StringMixin:
    def ends_with(self, suffix: str) -> StringMixin:
        if not self.value.endswith(suffix):
            self._failed(f"String: {self.value} did not end with: {suffix}")
        return self

    def starts_with(self, prefix: str) -> StringMixin:
        if not self.value.startswith(prefix):
            self._failed(f"String: {self.value} did not start with: {prefix}")
        return self
