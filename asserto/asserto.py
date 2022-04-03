import typing

from .mixins import StringMixin


class Asserto(StringMixin):
    """
    Core API
    """

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    @staticmethod
    def _failed(message: str) -> typing.NoReturn:
        __tracebackhide__ = True  # noqa
        raise AssertionError(message)
