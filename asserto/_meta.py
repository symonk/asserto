import inspect
import typing


class RouteMeta(type):
    """
    A Meta class for implicitly mapping callable methods against their handlers.  Bolts on an
    arbitrary dictionary into the instance that maps method names to handlers and appropriate
    error messages.
    """

    @staticmethod
    def __new__(cls, name, bases, attrs):
        instance = super().__new__(cls, name, bases, attrs)
        # Resolve all decorated methods and update the instance dictionary for dispatch.
        methods = inspect.getmembers(instance, lambda x: hasattr(x, "__handler__"))
        for methodname, methodobj in methods:
            instance._routes[methodname] = methodobj.__handler__
        return instance


def handled_by(handler: typing.Any):
    """
    Assigns an attribute on asserto functions that allow the metaclass to autopopulate the
    delegating handlers for each individual function.
    """

    def decorator(func):
        func.__handler__ = handler
        return func

    return decorator
