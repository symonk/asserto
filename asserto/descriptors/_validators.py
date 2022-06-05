import typing

from ._abc import Validatable


class IsCallable(Validatable):
    """
    A Simple check that an argument is a callable type.
    """

    def validate(self, value: typing.Any) -> None:
        if not callable(value):
            raise ValueError(f"{value} is not callable.")


T = typing.TypeVar("T")


class IsInstanceOf(Validatable, typing.Generic[T]):
    """Check if the value is an instance of multiple types."""

    def __init__(self, *types) -> None:
        self.types = types

    def validate(self, value: typing.Any) -> None:
        if not isinstance(value, self.types):
            raise ValueError(f"{value} was not an instance of any of: {self.types}")
