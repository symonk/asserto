import inspect
import typing


class AssertoMeta(type):
    """
    A Meta class for implicitly mapping callable methods against their handlers.  Bolts on an
    arbitrary dictionary into the instance that maps method names to handlers and appropriate
    error messages.
    """

    @staticmethod
    def __new__(cls, name, bases, attrs):
        # Bolton the _routes to the class of `Asserto`.
        clazz = super().__new__(cls, name, bases, attrs)
        # Resolve all decorated methods and update the instance dictionary for dispatch.

        def has_asserto_handler(m):
            metadata = getattr(m, "__asserto__", None)  # was decorated with @handled_by
            return metadata is not None and "handler" in metadata

        methods = inspect.getmembers(clazz, has_asserto_handler)
        for methodname, methodobj in methods:
            clazz._routing[methodname] = methodobj.__asserto__["handler"]
        return clazz


def handled_by(handler: typing.Type[typing.Any]):
    """
    Assigns an attribute on asserto functions that allow the metaclass populates the
    delegating handlers for each individual function.
    """

    def decorator(func):

        func.__asserto__ = {"handler": handler}
        return func

    return decorator
