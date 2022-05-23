import typing

from ._handler import Handler


class BaseHandler(Handler):
    """
    A handler for all objects.
    """

    def __init__(self, actual: typing.Any) -> None:
        super().__init__(actual)

    def is_true(self) -> None:
        if self.actual is False:
            raise AssertionError(f"{self.actual} was not True")

    def is_false(self) -> None:
        if self.actual is True:
            raise AssertionError(f"{self.actual} was not False")
