from __future__ import annotations

import inspect
import types
import typing
import warnings

from ._error_handling import ErrorHandler
from ._exceptions import DynamicCallableWithArgsError
from ._exceptions import InvalidHandlerTypeException
from ._messaging import Reason
from ._meta import AssertoBase
from ._meta import handled_by
from ._raising import ExceptionChecker
from ._types import EXC_TYPES_ALIAS
from ._types import RE_FLAGS_ALIAS
from ._types import RE_PATTERN_ALIAS
from ._util import is_namedtuple_like
from ._warnings import NoAssertAttemptedWarning
from .handlers import BaseHandler
from .handlers import RegexHandler
from .handlers import StringHandler

# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


class Asserto(AssertoBase):
    """
    The entrypoint into asserting objects.

    :param actual: ...
    :param warn_unused: ...
    """

    def __init__(self, actual: typing.Any, warn_unused: bool = False):
        self.actual = actual
        self._triggered = False
        self._reason = Reason()
        self._error_handler = ErrorHandler(self._reason)
        self.warn_unused = warn_unused

    def error(self, cause: typing.Union[AssertionError, str]) -> Asserto:
        """
        The single point of assertion failing.  All functions delegate here to raise the underlying
        assertion errors.
        :param cause: A reason for the failure. if description was set; it takes precedence.
        :return: The `Asserto` instance for fluency
        """
        __tracebackhide__ = True
        self._error_handler.error(cause)
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

    def set_category(self, category: str) -> Asserto:
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

    def should_raise(self, exceptions: EXC_TYPES_ALIAS) -> ExceptionChecker:
        """
        Wraps the actual value into a callable if it is callable itself;
        :param exceptions: The type of exception expected.
        :return: The `Asserto` instance for fluency
        """
        return ExceptionChecker(exc_types=exceptions, value=self.actual, _referent=self)

    # Todo: should_not_raise

    @handled_by(StringHandler)
    def ends_with(self, suffix: str) -> Asserto:
        """
        Asserts that the actual value ends with suffix.

        :param suffix: The suffix to compare the tail of the string against.
        """
        return self._dispatch(
            suffix,
        )

    @handled_by(StringHandler)
    def starts_with(self, prefix: str) -> Asserto:
        """
        Asserts that the actual value ends with prefix.

        :param prefix: The prefix to compare the head of the string against.
        """
        return self._dispatch(prefix)

    @handled_by(StringHandler)
    def is_digit(self) -> Asserto:
        """
        Asserts that the actual value contains only unicode letters and that the string has
        at least a single character.
        """
        return self._dispatch()

    @handled_by(StringHandler)
    def is_alpha(self) -> Asserto:
        """
        Asserts that the actual value contains only unicode letters and that the string has
        at least a single character.
        """
        return self._dispatch()

    def _dispatch(self, *args, **kwargs) -> Asserto:
        """
        Delegate a check to an underlying handler instance.

        :param error_template: (Optional) The error message to raise on failure.

        Arbitrary args & kwargs to pass through to the handler method.

        Note: Debugging this with an IDE can yield unrealistic as debugging tends to insert
        arbitrary code into the stack and this relies on frame inspection.
        """
        __tracebackhide__ = True
        caller = inspect.stack()[1][3]  # Todo: We need a better solution than this for future.
        self.triggered = True
        # for now allow this to be bypassed as not all methods have a handler defined.
        try:
            handler = self._routes[caller](self.actual)  # descriptors enforce types here.
        except ValueError:
            raise InvalidHandlerTypeException(f"function: {caller} does not support type: {type(self.actual)}")
        except KeyError:
            raise KeyError(f"{caller} does not have a dedicated handler.") from None
        assertion_method: typing.Optional[types.MethodType] = getattr(handler, caller)
        if assertion_method is None or not callable(assertion_method):
            raise TypeError(f"assertion method was not a bound method on the handler {handler}")
        try:
            _ = assertion_method(*args, **kwargs)
        except AssertionError as e:
            if description := self._reason.description:
                e = AssertionError(description)
            self.error(e)
        # Fall through type & value errors; we don't need to do anything in particular for them, just bubble em up.
        # (for now anyway).
        return self

    @handled_by(RegexHandler)
    def match(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> Asserto:
        """
        Asserts that the actual value provided matches (at least in part) from the beginning of it
        the pattern provided.  This is only a 'begins with' partial match.  Opt for `fullmatch` to
        perform a pattern match on the entirety of the actual value.

        :param pattern: The regular expression pattern to use; r"" is encouraged.
        :param flags: An integer (or RegexFlag) representing flags to apply.
        """
        return self._dispatch(pattern, flags)

    @handled_by(RegexHandler)
    def search(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> Asserto:
        """
        Asserts that the actual value provided has at least one single match of the pattern
        at some point within it.

        :param pattern: The regular expression pattern to use; r"" is encouraged.
        :param flags: An integer (or RegexFlag) representing flags to apply.
        """
        return self._dispatch(pattern, flags)

    @handled_by(RegexHandler)
    def fullmatch(self, pattern: RE_PATTERN_ALIAS, flags: RE_FLAGS_ALIAS = 0) -> Asserto:
        """
        Asserts that the actual value provided wholly matches the pattern provided. Providing
        `^` & `$` is not necessary as they are implicitly inferred.

        :param pattern: The regular expression pattern to use; r"" is encouraged.
        :param flags: An integer (or RegexFlag) representing flags to apply.
        """
        return self._dispatch(pattern, flags)

    @handled_by(RegexHandler)
    def findall(self, pattern: RE_PATTERN_ALIAS, count: int, flags: RE_FLAGS_ALIAS = 0) -> Asserto:
        """
        Asserts that the total count of non overlapping occurrences of pattern is equal to count.

        :param pattern: The regular expression pattern to use; r"" is encouraged.
        :param count: The expected number of elements expected in the fullmatch returned sequence.
        :param flags: An integer (or RegexFlag) representing flags to apply.
        """
        return self._dispatch(pattern, count, flags)

    @handled_by(BaseHandler)
    def is_true(self) -> Asserto:
        """
        Checks the actual value is True.
        :return: The `Asserto` instance for fluency.
        """
        return self._dispatch()

    @handled_by(BaseHandler)
    def is_false(self) -> Asserto:
        """
        Checks the actual value is False.
        :return: The `Asserto` instance for fluency.
        """
        return self._dispatch()

    @handled_by(BaseHandler)
    def is_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        return self._dispatch(other)

    @handled_by(BaseHandler)
    def is_not_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for non equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        return self._dispatch(other)

    @handled_by(BaseHandler)
    def has_length(self, expected: int) -> Asserto:
        """
        A simple check that the actual value is equal to expected utilising the built in `len(...)`

        :param expected: An int to compare the length against.
        :return: The instance of `Asserto` to chain asserts.
        """
        return self._dispatch(expected)

    @handled_by(BaseHandler)
    def is_instance(self, cls_or_tuple: typing.Union[typing.Any, typing.Iterable[typing.Any]]) -> Asserto:
        """
        Checks if the value provided is either:

            :: A direct subclass.
            :: An indirect subclass.
            :: A virtual subclass registered via the abc.

        :param cls_or_tuple: A single Type, or iterable of types to check the object against.
        """
        return self._dispatch(cls_or_tuple)

    @handled_by(BaseHandler)
    def has_same_identity_as(self, other: typing.Any) -> Asserto:
        """
        Checks that the value refers to the same object in memory as `other`.`
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        return self._dispatch(other)

    @handled_by(BaseHandler)
    def does_not_have_same_identity_as(self, other: typing.Any) -> Asserto:
        """
        Checks that the value does not refer to the same object in memory as `other`.
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        return self._dispatch(other)

    @handled_by(BaseHandler)
    def is_none(self) -> Asserto:
        """
        Checks the actual value is None.  Python `NoneType` is a singleton so `is` checks
        are used
        :return: The `Asserto` instance for fluency.
        """
        return self._dispatch()

    @handled_by(BaseHandler)
    def is_not_none(self) -> Asserto:
        """
        Checks the actual value is not None .  Python `None` is a singleton so `is not` checks are
        used.
        :return: The `Asserto` instance for fluency
        """
        return self._dispatch()

    @staticmethod
    def _warn_not_triggered() -> None:
        """
        Triggers a warning if an asserto instance was created and no assertion methods was called
        to highlight potential user errors.
        """
        warnings.warn("Asserto instance was created and never used", NoAssertAttemptedWarning, 2)

    def __getattr__(self, item: str) -> typing.Callable[[typing.Any], typing.Any]:
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
        if self.warn_unused and not self.triggered:
            self._warn_not_triggered()
        if self._error_handler.soft_errors:
            # There was a compilation of assertion errors
            errors = self._error_handler.soft_errors
            raise AssertionError(f"{len(errors)} Soft Assertion Failures, {errors}") from None
        self._error_handler.transition_to_hard()
