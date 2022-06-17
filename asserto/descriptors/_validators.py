import typing

from ._abc import Validatable


class EnforcedCallable(Validatable):
    """
    A Simple check that an argument is a callable type.
    """

    def validate(self, value: typing.Any) -> None:
        if not callable(value):
            raise ValueError(f"{value} is not callable.")


T = typing.TypeVar("T")


class ValidatesInstanceOf(Validatable, typing.Generic[T]):
    """Check if the value is an instance of multiple types."""

    def __init__(self, *types) -> None:
        self.types = types

    def validate(self, value: typing.Any) -> None:
        if isinstance(value, self.types) is False:
            raise ValueError(f"{value} was not an instance of any of: {self.types}")
