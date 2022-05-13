from __future__ import annotations

import inspect
import re
import types
import typing
import warnings

from ._decorators import update_triggered
from ._error_handling import ErrorHandler
from ._exceptions import DynamicCallableWithArgsError
from ._exceptions import ExpectedTypeError
from ._messaging import Reason
from ._meta import RouteMeta
from ._meta import handled_by
from ._raising_handler import Raises
from ._templates import Errors
from ._types import EXC_TYPES_ALIAS
from ._util import is_namedtuple_like
from ._warnings import NoAssertAttemptedWarning
from .handlers import StringHandler

# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


class Asserto(metaclass=RouteMeta):
    """
    The entrypoint into asserting objects.

    :param actual: The actual value
    """

    _routes: typing.Dict[str, typing.Any] = {}

    def __init__(
        self,
        actual: typing.Any,
    ):
        self.actual = actual
        self._triggered = False
        self._reason = Reason()
        self._error_handler = ErrorHandler(self._reason)

    def error(self, reason: str) -> Asserto:
        """
        The single point of assertion failing.  All functions delegate here to raise the underlying
        assertion errors.
        :param reason: A reason for the failure. if description was set; it takes precedence.
        :return: The `Asserto` instance for fluency
        """
        __tracebackhide__ = True
        self._error_handler.error(reason)
        return self

    @property
    def triggered(self) -> bool:
        """
        Check if the instance has invoked any methods that could have raised an `AssertionError`.
        :return: boolean indicating if a method has been invoked.
        """
        return self._triggered

    @triggered.setter
    def triggered(self, _) -> None:
        """
        Consider the asserto instance as `triggered`.  Instances which are instantiated but do not
        invoke any assertion methods will omit a warning as this usually indicates user error and
        helps to reduce mistakes in test code leading to misguided confidence in the test suite.
        :return: The `Asserto` instance for fluency.
        """
        self._triggered = True

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

    def should_raise(self, exceptions: EXC_TYPES_ALIAS) -> Raises:
        """
        Wraps the actual value into a callable if it is callable itself;
        :param exceptions: The type of exception expected.
        :return: The `Asserto` instance for fluency
        """
        return Raises(exc_types=exceptions, value=self.actual, _referent=self)

    # Todo: should_not_raise

    @handled_by(handler=StringHandler)
    def ends_with(self, suffix: str) -> Asserto:
        """
        Asserts that the actual value ends with suffix.

        :param suffix: The suffix to compare the tail of the string against.
        """
        return self._dispatch(
            Errors.strings.ends_with(actual=self.actual, expected=suffix),
            suffix,
        )

    @handled_by(handler=StringHandler)
    def starts_with(self, prefix: str) -> Asserto:
        """
        Asserts that the actual value ends with prefix.

        :param prefix: The prefix to compare the head of the string against.
        """
        return self._dispatch(
            Errors.str.starts_with(actual=self.actual, expected=prefix),
            prefix,
        )

    @handled_by(handler=StringHandler)
    def is_digit(self) -> Asserto:
        """
        Asserts that the actual value contains only unicode letters and that the string has
        at least a single character.
        """
        return self._dispatch(Errors.str.is_digit(actual=self.actual))

    @handled_by(handler=StringHandler)
    def is_alpha(self) -> Asserto:
        """
        Asserts that the actual value contains only unicode letters and that the string has
        at least a single character.
        """
        return self._dispatch(Errors.str.is_alpha(actual=self.actual))

    def _dispatch(self, on_fail: str, *args, **kwargs) -> Asserto:
        """
        Delegate a check to an underlying handler instance.

        :param handle_instance: The handler to delegate too.
        :param assertion_method: The method to invoke on the handler.
        :param on_fail: The error message to raise on failure.

        Arbitrary args & kwargs to pass through to the handler method.

        Note: Debugging this with an IDE can yield unrealistic as debugging tends to insert
        arbitrary code into the stack and this relies on
        """
        caller = inspect.stack()[1][3]  # Todo: We need a better solution than this for future.
        self.triggered = True
        # for now allow this to be bypassed as not all methods have a handler defined.
        try:
            handle_instance = self._routes[caller]()
        except KeyError:
            raise KeyError(f"{caller} does not have a dedicated handler.") from None
        assertion_method: typing.Optional[types.MethodType] = getattr(handle_instance, caller)
        if assertion_method is None or not callable(assertion_method):
            raise TypeError(f"assertion method was not a bound method on the handler {handle_instance}")
        # Enforce the guarding for the Handler.  Todo: I don't think this should be the responsibility here;
        handle_instance.matches_criterion(self.actual)
        if assertion_method(self.actual, *args, **kwargs) is False:
            self.error(on_fail)
        return self

    @update_triggered  # Todo: Go through dispatch
    def matches(self, pattern: str, flags: typing.Union[int, re.RegexFlag] = 0) -> Asserto:
        if re.match(rf"{pattern}", self.actual, flags) is None:
            self.error(f"{pattern} did not match the value: {self.actual}")
        return self

    @update_triggered  # Todo: Go through dispatch
    def is_true(self) -> Asserto:
        """
        Checks the actual value is True.
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is False:
            self.error(f"{self.actual!r} was not True")
        return self

    @update_triggered  # Todo: Go through dispatch
    def is_false(self) -> Asserto:
        """
        Checks the actual value is False.
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is True:
            self.error(f"{self.actual!r} was not False")
        return self

    @update_triggered  # Todo: Go through dispatch
    def is_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual != other:
            self.error(f"{self.actual!r} was not equal to: {other!r}")
        return self

    @update_triggered  # Todo: Go through dispatch
    def is_not_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for non equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual == other:
            self.error(f"{self.actual!r} is equal to: {other!r}")
        return self

    @update_triggered  # Todo: Go through dispatch
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

    @update_triggered  # Todo: Go through dispatch
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

    @update_triggered  # Todo: Go through dispatch
    def refers_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value refers to the same object in memory as `other`.`
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is not other:
            self.error(f"{self.actual!r} is not: {other!r}")
        return self

    @update_triggered  # Todo: Go through dispatch
    def does_not_refer_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value does not refer to the same object in memory as `other`.
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is other:
            self.error(f"{self.actual!r} points to the same memory location as: {other!r}")
        return self

    @update_triggered  # Todo: Go through dispatch
    def is_none(self) -> Asserto:
        """
        Checks the actual value is None.  Python `NoneType` is a singleton so `is` checks
        are used
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is not None:
            self.error(f"{self.actual!r} is not {None}")
        return self

    @update_triggered  # Todo: Go through dispatch
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
        warnings.warn("Asserto instance was created and never used", NoAssertAttemptedWarning, 2)

    def __del__(self) -> None:
        if not self.triggered:
            self._warn_not_triggered()

    def __getattr__(self, item: str) -> typing.Callable:
        """
        Adds the capability to object class or instance attributes dynamically.  Supports user defined
        object types as well as built in mapping types.  In the case of a mapping type the attribute
        name will be the key in the dictionary and value called its value to check for equality.

        :param item: The attribute name to lookup
        """
        if not item.endswith("_is"):
            raise AttributeError(f"unknown assertion method: {item}")
        key_attr = item[:-3]
        named_tuple_like = is_namedtuple_like(self.actual)
        mapping_like = isinstance(self.actual, typing.Iterable) and hasattr(self.actual, "__getitem__")
        failure = None

        if not hasattr(self.actual, key_attr):
            # It's not an attribute on the wrapped `actual` value.
            if not named_tuple_like and mapping_like:
                if key_attr not in self.actual:
                    failure = f"{self.actual!r} missing key: {key_attr}"
            else:
                failure = f"{self.actual!r} missing attribute: {key_attr}"

        def _dynamic_callable(*args):
            self.triggered = True  # Dynamic wrapper has been invoked!
            if failure:
                self.error(failure)
            if len(args) != 1:
                raise TypeError(f"Dynamic assertion takes 1 argument but {len(args)} was given. {args}")
            value = self.actual[key_attr] if not named_tuple_like and mapping_like else getattr(self.actual, key_attr)
            if callable(value):
                try:
                    lookup = value()
                except TypeError:
                    raise DynamicCallableWithArgsError(f"{key_attr} expects arguments, this is not supported") from None
            else:
                lookup = value
            expected = args[0]
            if lookup != expected:
                self.error(f"{lookup} was not equal to: {expected}")
            return self

        return _dynamic_callable

    def __repr__(self) -> str:
        return f"Asserto(value={self.actual}, category={self._reason.category})"

    def __enter__(self) -> Asserto:
        """
        Enter a `soft` context mode;  During this context `AssertionErrors` are silently
        ignored until the context is exited at which point any assertions will cause test
        failure(s) and raise the sequence of AssertionError's in the order in which they
        occurred.
        :return: The instance of `Asserto`.
        """
        self._error_handler.transition_to_soft()
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[types.TracebackType] = None,
    ):
        __tracebackhide__ = True
        if not self.triggered:
            self._warn_not_triggered()
        if self._error_handler.soft_fails:
            # There was a compilation of assertion errors
            raise AssertionError(self._error_handler.soft_fails) from None
        self._error_handler.transition_to_hard()
