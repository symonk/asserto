import typing
from typing import Protocol


class HasActual(Protocol):
    """A Protocol to aid with type hinting of mixin classes for assertion handlers."""

    @property
    def actual(self) -> typing.Any:
        return self.actual
