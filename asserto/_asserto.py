from __future__ import annotations

import re
import types
import typing
import warnings

from ._constants import AssertTypes
from ._decorators import triggered
from ._exceptions import ExpectedTypeError
from ._protocols import Reasonable
from ._states import State
from ._warnings import UntriggeredAssertoWarning

__tracebackhide__ = True


# Todo: base: `has_repr(...)`
# Todo: base: `descriptions`
# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


class Reason(Reasonable):
    """
    An encapsulation of assertion error messages.
    """

    def __init__(self, category: typing.Optional[str] = None, description: typing.Optional[str] = None) -> None:
        self.category = category
        self.description = description

    def format(self, reason: str) -> str:
        reason = self.description or reason
        if self.category:
            return f"[{self.category}] {reason}"
        return reason


class Asserto:
    """Asserto."""

    def __init__(
        self,
        actual: typing.Any,
        type_of: str = AssertTypes.HARD,
        state: typing.Type[State] = State,
        reason_supplier: typing.Type[Reason] = Reason,
    ):
        self.actual = actual
        self.type_of = type_of
        self._state = state()
        self._reason = reason_supplier()
        self._soft_failures = []

    def with_category(self, category: str) -> Asserto:
        """
        Set the category for the assertion.  Categories are prefixed to the assertion
        messages, for example:

            Example:
                Usage::
                    asserto(25).with_category("foo").is_equal_to(26)
                    `AssertionError(["foo"] 25 was not equal to: 26)`

        :param category: The Category to group the assertion under.
        :return: The `Asserto` instance for fluency.
        """
        self._reason.category = category
        return self

    def described_as(self, description: str) -> Asserto:
        """
        Set the full `AssertionError`` message to a custom reason.  If this is
        invoked anything after the category (if also set) will be user defined.
        :param description: The reason to display if an `AssertionError` is raised.
        :return: The `Asserto` instance for fluency.
        """
        self._reason.description = description
        return self

    @triggered
    def ends_with(self, suffix: str) -> Asserto:
        """
        Asserts that the value provided begins with the suffix.
        :param suffix: A substring to ensure the value begins with.
        """
        if not self.actual.endswith(suffix):
            self.error(f"{self.actual} did not end with {suffix}")
        return self

    @triggered
    def starts_with(self, prefix: str) -> Asserto:
        if not self.actual.startswith(prefix):
            self.error(f"{self.actual} did not start with {prefix}")
        return self

    @triggered
    def matches(self, pattern: str) -> Asserto:
        if re.match(re.compile(rf"{pattern}"), self.actual) is None:
            self.error(f"{pattern} did not match the value: {self.actual}")
        return self

    @triggered
    def is_true(self) -> Asserto:
        """
        Checks the actual value is True.
        :return: The `Asserto` instance for fluency.
        """
        if not self.actual:
            self.error(f"{self.actual!r} was not True")
        return self

    @triggered
    def is_false(self) -> Asserto:
        """
        Checks the actual value is False.
        :return: The `Asserto` instance for fluency.
        """
        if self.actual:
            self.error(f"{self.actual!r} was not False")
        return self

    @triggered
    def is_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual != other:
            self.error(f"{self.actual!r} was not equal to: {other!r}")
        return self

    @triggered
    def is_not_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for non equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual == other:
            self.error(f"{self.actual!r} is equal to: {other!r}")
        return self

    @triggered
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

    @triggered
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

    @triggered
    def refers_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value refers to the same object in memory as `other`.`
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is not other:
            self.error(f"{self.actual!r} is not: {other!r}")
        return self

    @triggered
    def does_not_refer_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value does not refer to the same object in memory as `other`.
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is other:
            self.error(f"{self.actual!r} points to the same memory location as: {other!r}")
        return self

    @triggered
    def is_none(self) -> Asserto:
        """
        Checks the actual value is None.  Python `NoneType` is a singleton so `is` checks
        are used
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is not None:
            self.error(f"{self.actual!r} is not {None}")
        return self

    @triggered
    def is_not_none(self) -> Asserto:
        """
        Checks the actual value is not None .  Python `None` is a singleton so `is not` checks are
        used.
        :return: The `Asserto` instance for fluency
        """
        if self.actual is None:
            self.error(f"{self.actual!r} is {None}")
        return self

    @staticmethod
    def _warn_not_triggered() -> None:
        """
        Triggers a warning if an asserto instance was created and no assertion methods was called
        to highlight potential user errors.
        """
        warnings.warn("Asserto instance was created and never used", UntriggeredAssertoWarning, 2)

    def __del__(self) -> None:
        if not self._state.triggered:
            self._warn_not_triggered()

    def error(self, reason: str) -> typing.NoReturn:
        raise AssertionError(self._reason.format(reason))

    def __repr__(self) -> str:
        return f"Asserto(value={self.actual}, type_of={self.type_of}, category={self._reason.category})"

    def __enter__(self) -> Asserto:
        """
        Enter a `soft` context mode;  During this context `AssertionErrors` are silently
        ignored until the context is exited at which point any assertions will cause test
        failure(s) and raise the sequence of AssertionError's in the order in which they
        occurred.
        :return: The instance of `Asserto`.
        """
        self._state.context = True
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ):
        # Todo: Implement the concept of 'soft' assertions using `Asserto` as a context
        self._state.context = False
        if not self._state.triggered:
            self._warn_not_triggered()
