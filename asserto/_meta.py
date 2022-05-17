import inspect
import typing

from .handlers import Handler


class AssertoBase:
    """
    Implicitly populates a `_routes` class attribute with all methods decorated by the
    @handled_by decorator for subsequent lookups via _dispatch(...).
    """

    _routes: typing.Dict[str, typing.Type[Handler]] = {}

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        method_info = inspect.getmembers(cls, predicate=lambda m: hasattr(m, "__handler__"))
        cls._routes = {name: obj.__handler__ for name, obj in method_info}


def handled_by(handler: typing.Type[Handler]):
    """
    Assigns an attribute on asserto functions that allow the metaclass populates the
    delegating handlers for each individual function.

    :param handler: A Handler class instance to be registered for the given method.
    """

    def decorator(func):
        func.__handler__ = handler
        return func

    return decorator
