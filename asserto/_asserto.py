from __future__ import annotations

import re
import types
import typing
import warnings

from ._constants import AssertTypes
from ._decorators import triggered
from ._exceptions import ExpectedTypeError
from ._messaging import ComposedFailure
from ._messaging import Reason
from ._states import State
from ._warnings import UntriggeredAssertoWarning

# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


class Asserto:
    """
    The entrypoint into asserting objects.

    :param actual: The actual value
    """

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
        self._soft_failures = ComposedFailure()

    def with_category(self, category: str) -> Asserto:
        """
        Set the category for the assertion.  Categories are prefixed to the assertion
        messages, for example:

            Example:
                Usage::
                    asserto(25).with_category("foo").is_equal_to(26)
                    `AssertionError(["foo"] 25 was not equal to: 26)`
        Args:
            category: The Category to group the assertion under.
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
    def matches(self, pattern: str, flags: typing.Union[int, re.RegexFlag] = 0) -> Asserto:
        if re.match(rf"{pattern}", self.actual, flags) is None:
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

    def error(self, reason: str) -> Asserto:
        error = AssertionError(self._reason.format(reason))
        if self._state.context:
            self._soft_failures.register_error(error)
            return self
        raise error from None

    def __getattr__(self, item: str) -> typing.Callable:
        """
        Adds the capability to object class or instance attributes dynamically.  Supports user defined
        object types as well as built in mapping types.  In the case of a mapping type the attribute 
        name will be the key in the dictionary and value called its value to check for equality.
        
        :param item: The attribute name to lookup
        """
        if not item.endswith("_is"):
            # Todo: [unit test #1]
            raise AttributeError(f"unknown assertion method: {item}")
        keyattr = item[:-3]
        is_namedtuple = self._is_namedtuple(self.actual)
        is_map_like = isinstance(self.actual, typing.Iterable) and hasattr(self.actual, "__getitem__")
        failure = None
        
        if not hasattr(self.actual, keyattr):
            if not is_namedtuple and is_map_like:
                if keyattr not in self.actual:
                    failure = f"{self.actual!r} does not contain the key: {keyattr}"
            else:
                failure = f"{self.actual!r} does not have a {keyattr} attribute"
                
        def _wrap_it(*args):
            if failure:
                self.error(failure)
            if len(args) != 1:
                # Todo: Copy pytests `__new__` for error message.
                raise TypeError(f"Dynamic assertions only support a single argument, but {len(args)} was given, {args}")
            value = self.actual[keyattr] if not is_namedtuple and is_map_like else getattr(self.actual, keyattr)
            if callable(value):
                try:
                    lookup = value()
                except TypeError:
                    # lookup is not a bound method / callable etc
                    raise TypeError(...)
            else:
                lookup = value
            if lookup != args[0]:
                self.error("Todo: A proper error message Here!")
            return self
        return _wrap_it
        
    def _is_namedtuple(self, obj) -> bool:
        # Todo: [unit test #2]
        t = type(obj)
        bases = t.__bases__
        if len(bases) != 1 and bases[0] != tuple:
            return False
        fields = getattr(obj, "_fields", None)
        if not isinstance(fields, tuple):
            return False
        return all(type(f) == str for f in fields)
        

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
        self._soft_failures = ComposedFailure()  # Force this to be reset.
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ):
        self._state.context = False
        if not self._state.triggered:
            self._warn_not_triggered()
        if self._soft_failures:
            # There was a compilation of assertion errors
            raise AssertionError(self._soft_failures)
