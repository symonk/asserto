import inspect
import typing

def guard_type_from_method(argument: typing.Any, check_type: typing.Any) -> None:
    """Ensures a particular object has an expected type else raises
    a Type error including the caller of this functions name. This
    should typically only be called by a mixin method performing
    an assertion.
    
    This unwinds the call stack to derive this information.
    
    :param argument: The object to check the type of.
    :param check_type: The type it should be of."""
    __tracebackhide__ = True
    current_frame = inspect.currentframe()
    caller = inspect.getouterframes(current_frame, 2)
    method_name = caller[1][3]
    arg_name: str = ""
    if not isinstance(argument, check_type):
        raise TypeError(f"[{method_name}] {arg_name} must be of type {check_type} but was: {type(argument)}.")