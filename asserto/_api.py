import types
import typing

from ._asserto import Asserto
from ._constants import AssertTypes


def asserto(actual: typing.Any, type_of: str = AssertTypes.HARD) -> Asserto:
    """
    Retrieve an appropriate asserter for the type of value.
    :param actual: The value to compare against later and defer a type specific asserter from.
    :param type_of: ...
    :return: An instance of an asserter
    """
    return Asserto(actual, type_of)


def bind(function: typing.Callable[[Asserto, typing.Any], typing.Any]) -> None:
    """
    # Todo: There is a lot of edge cases here that I'm not (yet) aware of.
    Registers a user defined `callable` function and binds it to all future instances
    of asserto.  The function should accept an `Asserto` instance as it's first parameter
    and use the asserto instances `.error(...)` method for handling its failing case.

    This allows user defined functions to be available to asserto.

    Example:
        Usage::
            # a contrived and relatively useless example
            def is_length_5(self):
                self.has_length(5)

            from asserto import extend
            bind(is_length_5)

            from asserto import Asserto

            Asserto((1,2,3)).is_length_5()

    :param function: A new function to be bound to `Asserto` instances.
    :return: None.
    """
    if not isinstance(function, types.FunctionType):
        raise ValueError("Binding functions must be of function types.")
    name = getattr(function, "__name__")
    # Todo: Can FunctionTypes have no __name__ ?
    if name.endswith("_is"):
        # Due to how asserto handles its dynamic lookups;
        raise ValueError("Binding functions cannot end with `_is`")
    if name == "<lambda>":
        raise ValueError("Binding functions does not support lambdas, they have no name")
    # Register a new function to the class.
    setattr(Asserto, name, function)
