import typing

from ._protocols import Assertable

__tracebackhide__ = True


class AsserterMixin(Assertable):
    def error(self, reason: str, description: typing.Optional[str] = None) -> typing.NoReturn:
        msg_with_desc = f"[{reason}] {reason}" if description else reason
        raise AssertionError(msg_with_desc)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(actual={self.actual!r})"
