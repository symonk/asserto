import types
import typing

from ._asserto import Asserto
from ._decorators import update_triggered


def asserto(actual: typing.Any, warn_unused: bool = False) -> Asserto:
    """
    Retrieve an appropriate asserter for the type of value.
    :param actual: The value to compare against later and defer a type specific asserter from.
    :param warn_unused: Emit a warning if not a single assertion was performed to detect user errors.
    :return: An instance of an asserter
    """
    return Asserto(actual, warn_unused)


def register_assert(func: types.FunctionType) -> typing.Callable[[typing.Any], typing.Any]:
    """
    # Todo: There is a lot of edge cases here that I'm not (yet) aware of.
    Automatically registers a user defined callable (function) to all future instances of Asserto.
    This is done magically using setattr and the functions must be imported before instantiating
    instances of Asserto to benefit from them,  store your custom assertion functions somewhere
    loaded early in your code and bind them before instantiating `Asserto` instances.

    Some criteria for user defined assertion functions must be met:
        :: They must use a `self` param first which will be an instance of Asserto
        :: They must be function types with a distinct __name__ to avoid overwriting existing attrs
        :: They must NOT be lambda functions as they have no distinct __name__
        :: They must NOT end in _is as Asserto does some dynamic dispatch using __getattr__ relying on that

    assertable can be called directly and passed your function, or apply it as a decorator to your
    assertion methods.  Examples of both cases are:

        Examples
            :: Usage

            from asserto import assertable

            @register_assert  # Option 1.
            def custom_assert(self):
                if not isinstance(self.actual, MyClass):
                    self.error("my assertion error message")

            register_assert(custom_assert)  # Option 2.
    """
    if not isinstance(func, types.FunctionType):
        raise ValueError("Binding functions must be of function types.")
    name = getattr(func, "__name__")
    # Todo: Can FunctionTypes have no __name__ ?
    if name.endswith("_is"):
        # Due to how asserto handles its dynamic lookups;
        raise ValueError("Binding functions cannot end with `_is`")
    if name == "<lambda>":
        raise ValueError("Binding functions does not support lambdas, they have no name")
    # Register a new function to the class.
    setattr(Asserto, name, update_triggered(func))
    return func
