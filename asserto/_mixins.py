import typing

from ._protocols import Assertable


class AsserterMixin(Assertable):
    def error(self, reason: str, description: typing.Optional[str] = None) -> typing.NoReturn:
        msg_with_desc = f"[{reason}] {reason}" if description else reason
        raise AssertionError(msg_with_desc)
