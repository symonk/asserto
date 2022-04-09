import functools
import typing


def triggered(fn: typing.Callable) -> typing.Callable:
    """
    Track the triggered state on any asserto calls to ensure no instances were created
    and used without calling any assertable methods.
    :param fn: The asserting function
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> typing.Callable:
        instance = args[0]
        result = fn(*args, **kwargs)
        instance._state.triggered = True
        return result

    return wrapper
