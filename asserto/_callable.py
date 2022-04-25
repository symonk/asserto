import typing

from ._descriptors import IsCallable
from ._types import EXC_TYPES_ALIAS
from ._util import to_iterable

__tracebackhide__ = True


class Raises:
    """
    Encapsulation of the asserto callable exception handling syntax.
    """

    _proxy_val = IsCallable()

    def __init__(
        self, exc_types: EXC_TYPES_ALIAS, value: typing.Callable[[typing.Any, ...], typing.Any], _referent
    ) -> None:
        self.exc_types = to_iterable(exc_types)
        self._proxy_val = value
        self.asserto_ref = _referent  # Todo: investigate weakref here.

    def when_called_with(self, *args, **kwargs) -> None:
        """
        Call the underlying function with the user supplied arguments;  This returns the result
        of the function back to the asserto instance to enforce error handling & assertion errors
        there.
        """
        try:
            # update 'triggered' status to avoid unnecessary warnings
            self.asserto_ref.triggered = True
            _ = self._proxy_val(*args, **kwargs)
            self.asserto_ref.error(f"{self._proxy_val} never raised any of: {self.exc_types}")
        except self.exc_types:
            # exception was raised as expected; no-op
            ...
