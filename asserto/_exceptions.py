"""
Asserto exception hierarchy.
    * ActualTypeError
"""


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
