"""
Asserto exception hierarchy.
    * ActualTypeError
"""


class ActualTypeError(TypeError):
    """Raised when type error problems occur with the actual value"""


class ExpectedTypeError(TypeError):
    """Raised when type error problems occur with the expected value"""
