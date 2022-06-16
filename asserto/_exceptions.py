"""
Asserto exception hierarchy.
    * ActualTypeError
"""
import typing

from .handlers import Handler


class ActualTypeError(TypeError):
    """Raised when type error problems occur with the actual value"""


class ExpectedTypeError(TypeError):
    """Raised when type error problems occur with the expected value"""


class DynamicCallableWithArgsError(TypeError):
    """
    Raised when a dynamic lookup via `attr_is` returns a callable that expects arguments.
    Asserto currently only supports 0-arg callables as part of its dynamic lookup and
    invocations.
    """


class InvalidHandlerTypeException(ValueError):
    """Raised when the actual value provided is not supported by the assertion method invoked by the caller."""

    def __init__(self, handler: typing.Type[Handler], method: str, value: typing.Any) -> None:
        super().__init__(f"`{handler.__name__}` cannot accept type: {type(value)} when calling: {method}")


class AssertoTypeViolation(TypeError):
    """ Raised when argument values passed to assertion methods fail on expected types. """
