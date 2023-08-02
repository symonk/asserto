import inspect
import typing

from ._const import ACTUAL_TYPE_ERROR


def enforce_type_of(object: typing.Any, types: typing.Any) -> None:
    """Ensures a particular object has an expected type else raises
    a Type error including the caller of this functions name. This
    should typically only be called by a mixin method performing
    an assertion.

    This unwinds the call stack to derive this information.

    :param object: The object to check the type of.
    :param types: The type it should be of."""
    __tracebackhide__ = True
    current_frame = inspect.currentframe()
    caller = inspect.getouterframes(current_frame, 2)
    method_name = caller[1][3]
    if not isinstance(object, types):
        raise TypeError(ACTUAL_TYPE_ERROR.format(object, types, method_name, type(object)))
