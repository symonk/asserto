from __future__ import annotations

import re

__tracebackhide__ = True


from .._mixins import AsserterMixin


class AssertsRegex(AsserterMixin):
    def __init__(self, actual: str) -> None:
        self.actual = actual

    def matches(self, pattern: str) -> None:
        if re.match(re.compile(rf"{pattern}"), self.actual) is None:
            self.error(f"{pattern} did not match the value: {self.actual}")
