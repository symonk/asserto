from typing import Any
from typing import Protocol
from typing import Union


class HasActualValue(Protocol):
    """A simple interface for something containing a `actual` value.
    This helps to support static type hinting with the mixins used
    to compose asserto."""

    @property
    def actual(self) -> Any:
        ...


class CanError(Protocol):
    """A simple interface for something that can raise an AssertionError."""

    def error(self, cause: Union[AssertionError, str]) -> Any:
        ...


class Assertable(HasActualValue, CanError):
    ...
