from __future__ import annotations

import re
import types
import typing
import warnings

from ._constants import AssertTypes
from ._decorators import update_triggered
from ._exceptions import ExpectedTypeError
from ._exceptions import DynamicCallableWithArgsError
from ._messaging import ComposedFailure
from ._messaging import Reason
from ._raising_handler import Raises
from ._states import State
from ._types import EXC_TYPES_ALIAS
from ._util import is_namedtuple_like
from ._warnings import NoAssertAttemptedWarning

# Todo: base: `tidy up docstrings`
# Todo: base `remove duplication here`


def register_assert(
    func: typing.Callable[[Asserto, typing.Any], typing.Any]
) -> typing.Callable[[typing.Any], typing.Any]:
    """
    # Todo: There is a lot of edge cases here that I'm not (yet) aware of.
    Automatically registers a user defined callable (function) to all future instances of Asserto.
    This is done magically using setattr and the functions must be imported before instantiating
    instances of Asserto to benefit from them,  store your custom assertion functions somewhere
    loaded early in your code and bind them before instantiating `Asserto` instances.

    Some criteria for user defined assertion functions must be met:
        :: They must use a `self` param first which will be an instance of Asserto
        :: They must be function types with a distinct __name__ to avoid overwriting existing attrs
        :: They must NOT be lambda functions as they have no distinct __name__
        :: They must NOT end in _is as Asserto does some dynamic dispatch using __getattr__ relying on that

    assertable can be called directly and passed your function, or apply it as a decorator to your
    assertion methods.  Examples of both cases are:

        Examples
            :: Usage

            from asserto import assertable

            @assertable  # Option 1.
            def custom_assert(self):
                if not isinstance(self.actual, MyClass):
                    self.error("my assertion error message")

            assertable(custom_assert)  # Option 2.
    """
    if not isinstance(func, types.FunctionType):
        raise ValueError("Binding functions must be of function types.")
    name = getattr(func, "__name__")
    # Todo: Can FunctionTypes have no __name__ ?
    if name.endswith("_is"):
        # Due to how asserto handles its dynamic lookups;
        raise ValueError("Binding functions cannot end with `_is`")
    if name == "<lambda>":
        raise ValueError("Binding functions does not support lambdas, they have no name")
    # Register a new function to the class.
    setattr(Asserto, name, func)
    return update_triggered(func)


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
        self._triggered = False
        self._reason = reason_supplier()
        self._soft_failures = ComposedFailure()

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

    @update_triggered
    def ends_with(self, suffix: str) -> Asserto:
        """
        Asserts that the value provided begins with the suffix.
        """
        if not self.actual.endswith(suffix):
            self.error(f"{self.actual} did not end with {suffix}")
        return self

    @update_triggered
    def starts_with(self, prefix: str) -> Asserto:
        if not self.actual.startswith(prefix):
            self.error(f"{self.actual} did not start with {prefix}")
        return self

    @update_triggered
    def matches(self, pattern: str, flags: typing.Union[int, re.RegexFlag] = 0) -> Asserto:
        if re.match(rf"{pattern}", self.actual, flags) is None:
            self.error(f"{pattern} did not match the value: {self.actual}")
        return self

    @update_triggered
    def is_true(self) -> Asserto:
        """
        Checks the actual value is True.
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is False:
            self.error(f"{self.actual!r} was not True")
        return self

    @update_triggered
    def is_false(self) -> Asserto:
        """
        Checks the actual value is False.
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is True:
            self.error(f"{self.actual!r} was not False")
        return self

    @update_triggered
    def is_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual != other:
            self.error(f"{self.actual!r} was not equal to: {other!r}")
        return self

    @update_triggered
    def is_not_equal_to(self, other: typing.Any) -> Asserto:
        """
        Compares the value against `other` for non equality.

        :param other: The other object to compare against.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual == other:
            self.error(f"{self.actual!r} is equal to: {other!r}")
        return self

    @update_triggered
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

    @update_triggered
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

    @update_triggered
    def refers_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value refers to the same object in memory as `other`.`
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is not other:
            self.error(f"{self.actual!r} is not: {other!r}")
        return self

    @update_triggered
    def does_not_refer_to(self, other: typing.Any) -> Asserto:
        """
        Checks that the value does not refer to the same object in memory as `other`.
        :param other: The other object to compare identity of.
        :return: The instance of `Asserto` to chain asserts.
        """
        if self.actual is other:
            self.error(f"{self.actual!r} points to the same memory location as: {other!r}")
        return self

    @update_triggered
    def is_none(self) -> Asserto:
        """
        Checks the actual value is None.  Python `NoneType` is a singleton so `is` checks
        are used
        :return: The `Asserto` instance for fluency.
        """
        if self.actual is not None:
            self.error(f"{self.actual!r} is not {None}")
        return self

    @update_triggered
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

    def error(self, reason: str) -> Asserto:
        """
        The single point of assertion failing.  All functions delegate here to raise the underlying
        assertion errors.
        :param reason: A reason for the failure. if self.description was set; it takes precedence.
        :return: The `Asserto` instance for fluency
        """
        __tracebackhide__ = True
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
        __tracebackhide__ = True
        self._state.context = False
        if not self.triggered:
            self._warn_not_triggered()
        if self._soft_failures:
            # There was a compilation of assertion errors
            raise AssertionError(self._soft_failures) from None
