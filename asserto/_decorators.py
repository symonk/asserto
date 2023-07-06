import functools
import typing

from ._constants import MixinErrorTemplates
from ._protocols import Assertable


def update_triggered(fn: typing.Callable[[typing.Any], typing.Any]) -> typing.Callable[[typing.Any], typing.Any]:
    """
    Track the triggered state on any asserto calls to ensure no instances were created
    and used without calling any assertable methods.
    :param fn: The asserting function
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> typing.Callable[[typing.Any], typing.Any]:
        instance = args[0]
        instance.triggered = True
        return fn(*args, **kwargs)

    return wrapper


def enforce_actual_has_type_of(
    expected_types: typing.Union[typing.Type[typing.Any], typing.Tuple[typing.Type[typing.Any], ...]]
):
    """Decorator that guards the self.actual type for mixin
    methods to avoid repetitive checks on self.actuals type.

    :param expected_types: An iterable of types to check via isinstance.
    """

    def deco(fn: typing.Callable[[typing.Any, typing.Any], Assertable]):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            instance = args[0]
            actual = instance.actual
            if not isinstance(actual, expected_types):
                method_name = fn.__name__
                raise TypeError(
                    MixinErrorTemplates.ASSERTO_TYPE_ERROR.format(actual, expected_types, method_name, type(actual))
                )
            return fn(*args, **kwargs)

        return wrapper

    return deco
