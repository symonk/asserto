from __future__ import annotations

import types
import typing

from ._constants import AssertTypes
from ._exceptions import ExpectedTypeError
from ._mixins import AsserterMixin
from .assertors import AssertsRegex
from .assertors import AssertsStrings

__tracebackhide__ = True


# Todo: base: `is_none()` & `is_not_none()`
# Todo: base: `has_repr(...)`
# Todo: base: `is_true() & is_false()`
# Todo: base: `descriptions`
# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


class Asserto(AsserterMixin):
    """Asserto."""

    def __init__(
        self,
        actual: typing.Any,
        type_of: str = AssertTypes.HARD,
        description: typing.Optional[str] = None,
        string_asserter: typing.Type[AssertsStrings] = AssertsStrings,
        regex_asserter: typing.Type[AssertsRegex] = AssertsRegex,
    ):
        self.actual = actual
        self.type_of = type_of
        self.description = description
        self.string_asserter = string_asserter(self.actual)
        self.regex_asserter = regex_asserter(self.actual)
        self._in_context = False
        self._soft_failures = []

    # ----- String Delegation -----
    def ends_with(self, suffix: str) -> Asserto:
        """
        Asserts that the value provided begins with the suffix.
        :param suffix: A substring to ensure the value begins with.
        """
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

    # ----- Start of Generic Delegation -----

    def is_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual != other:
            self.error(f"{self.actual!r} was not equal to: {other!r}")
        return self

    def is_not_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for non equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual == other:
            self.error(f"{self.actual!r} is equal to: {other!r}")
        return self

    def has_length(self, expected: int) -> Asserto:
        """
        A simple check that the actual value is equal to expected utilising the built in `len(...)`

        :param expected: An int to compare the length against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if not isinstance(expected, int) or expected < 0:
            raise ExpectedTypeError(f"{expected!r} must be an int and greater than 0")

        if len(self.actual) != expected:
            self.error(f"Length of: {self.actual!r} was not equal to: {expected!r}")
        return self

    def is_instance(self, cls_or_tuple: typing.Union[typing.Any, typing.Iterable[typing.Any]]) -> Asserto:
        """
        Checks if the value provided is either:

            :: A direct subclass.
            :: An indirect subclass.
            :: A virtual subclass registered via the abc.

        :param cls_or_tuple: A single Type, or iterable of types to check the object against.
        """
        if not isinstance(self.actual, cls_or_tuple):
            self.error(f"[{self.actual!r}]: {type(self.actual)} was not an instance of: {cls_or_tuple}")
        return self

    def refers_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value refers to the same object in memory as `other`.`
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is not other:
            self.error(f"{self.actual!r} is not: {other!r}")
        return self

    def does_not_refer_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value does not refer to the same object in memory as `other`.
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is other:
            self.error(f"{self.actual!r} points to the same memory location as: {other!r}")
        return self

    def is_none(self) -> Asserto:
        """
        Checks the actual value is None.  Python `NoneType` is a singleton so `is` checks
        are used
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is not None:
            self.error(f"{self.actual!r} is not {None}")
        return self

    def is_not_none(self) -> Asserto:
        """
        Checks the actual value is not None .  Python `None` is a singleton so `is not` checks are
        used.
        :return: The `Asserto` instance for fluency
        """
        if self.actual is None:
            self.error(f"{self.actual!r} is {None}")
        return self

    # ----- End of Generic Delegation -----

    # ----- Start of Dunder Methods -----

    def __repr__(self) -> str:
        return f"Asserto(value={self.actual}, type_of={self.type_of}, description={self.description})"

    def __enter__(self) -> Asserto:
        """
        Enter a `soft` context mode;  During this context `AssertionErrors` are silently
        ignored until the context is exited at which point any assertions will cause test
        failure(s) and raise the sequence of AssertionError's in the order in which they
        occurred.
        :return: The instance of `Asserto`.
        """
        self._in_context = True  # Know we are being used as a context.
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ):
        # Todo: Implement the concept of 'soft' assertions using `Asserto` as a context
        self._in_context = False

    # ----- end of dunder -----
