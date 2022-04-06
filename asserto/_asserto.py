from __future__ import annotations

import types
import typing

from ._constants import AssertTypes
from ._mixins import AsserterMixin
from ._types import TYPE_ALIAS
from .assertors import AssertsRegex
from .assertors import AssertsStrings

__tracebackhide__ = True


class Asserto(AsserterMixin):
    """
    Core API

    Todos:
        :: is_true()
        :: is_false()
        :: is_none()
        :: is_not_none()
        :: is_type_of()
        :: is_subclass_of? (maybe is_instance covers it?)
        :: is_not_equal_to()
    """

    def __init__(
        self,
        value: typing.Any,
        type_of: str = AssertTypes.HARD,
        description: typing.Optional[str] = None,
        string_asserter: typing.Type[AssertsStrings] = AssertsStrings,
        regex_asserter: typing.Type[AssertsRegex] = AssertsRegex,
    ):
        self.value = value
        self.type_of = type_of
        self.description = description
        self.string_asserter = string_asserter(self.value)
        self.regex_asserter = regex_asserter(self.value)

    # ----- String Delegation -----
    def ends_with(self, suffix: str) -> Asserto:
        self.string_asserter.ends_with(suffix)
        return self

    def starts_with(self, suffix: str) -> Asserto:
        self.string_asserter.starts_with(suffix)
        return self

    # ----- End of String Delegation -----

    # ----- Regex Delegation -----
    def matches(self, pattern: str) -> Asserto:
        self.regex_asserter.matches(pattern)
        return self

    # ----- End of Regex Delegation -----

    def __repr__(self) -> str:
        return f"Asserto(value={self.value}, type_of={self.type_of}, description={self.description})"

    def is_equal_to(self, value: typing.Any) -> Asserto:
        # Todo: Make all of these generic checks 'realistic', they aren't actually fit for purpose atm.
        """
        General object comparison.
        :param value: The value to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.value != value:
            self.error(f"{self.value} was not equal to: {value}")
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

    def has_same_id_as(self, value: TYPE_ALIAS) -> Asserto:
        # Todo: Make all of these generic checks 'realistic', they aren't actually fit for purpose atm.
        """
        General pointer comparison, compare by object ID.
        :param value: The other object to compare.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.value is not value:
            self.error(f"{self.value} is not: {value}")
        return self

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
