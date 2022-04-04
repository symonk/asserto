from __future__ import annotations

import types
import typing

from ._constants import AssertTypes
from ._types import TYPE_ALIAS
from .mixins import StringMixin
from .mixins import RegexMixin

__tracebackhide__ = True


class Asserto(StringMixin, RegexMixin):
    """
    Core API
    """

    def __init__(self, value: typing.Any, type_of: str = AssertTypes.HARD, description: typing.Optional[str] = None):
        self.value = value
        self.type_of = type_of
        self.description = description

    def __repr__(self) -> str:
        return f"Asserto(value={self.value}, type_of: {self.type_of}, description: {self.description})"

    def equals(self, value: typing.Any) -> Asserto:
        # Todo: Make all of these generic checks 'realistic', they aren't actually fit for purpose atm.
        """
        General object comparison.
        :param value: The value to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.value != value:
            self.error(f"{self.value} was not equal to: {value}")
        return self

    def has_same_identity_of(self, value: TYPE_ALIAS) -> Asserto:
        # Todo: Make all of these generic checks 'realistic', they aren't actually fit for purpose atm.
        """
        General pointer comparison, compare by object ID.
        :param value: The other object to compare.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.value is not value:
            self.error(f"{self.value} is not: {value}")
        return self

    def is_length(self, length: int) -> Asserto:
        # Todo: Make all of these generic checks 'realistic', they aren't actually fit for purpose atm.
        if len(self.value) != length:
            self.error(f"Length of: {self.value} was not equal to length of: {length}")
        return self

    def is_instance(self, cls_or_tuple: typing.Union[TYPE_ALIAS, typing.Iterable[TYPE_ALIAS]]) -> Asserto:
        """
        Checks if the value provided is either:
            :: Is a direct subclass instance of at least one of the types in cls_or_tuple.
            :: Is an indirect subclass instance of at least one of the types in cls_or_tuple.
            :: Is a virtual subclass instance of at least one of the types in cls_or_tuple.
        :param cls_or_tuple: A single Type, or iterable of types to check the object against.
        """
        if not isinstance(self.value, cls_or_tuple):
            self.error(f"[{self.value!r}]: {type(self.value)} was not an instance of: {cls_or_tuple}")
        return self

    def error(self, message: str) -> typing.NoReturn:
        msg_with_desc = f"[{self.description}] {message}" if self.description else message
        raise AssertionError(msg_with_desc)

    def __enter__(self) -> Asserto:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ):
        # Todo: Implement the concept of 'soft' assertions using `Asserto` as a context
        ...
