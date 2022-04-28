import functools
import typing


def update_triggered(fn: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Any], typing.Any]:
    """
    Track the triggered state on any asserto calls to ensure no instances were created
    and used without calling any assertable methods.
    :param fn: The asserting function
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> typing.Callable[[typing.Any], typing.Any]:
        instance = args[0]
        try:
            result = fn(*args, **kwargs)
        finally:
            instance.triggered = True
        return result

    return wrapper
