from __future__ import annotations
import re


__tracebackhide__ = True


class RegexMixin:

    def matches(self, pattern: str) -> RegexMixin:
        if re.match(re.compile(rf"{pattern}"), self.value) is None:
            self.error(f"{pattern} did not match the value: {self.value}")
        return self
