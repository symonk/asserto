import typing

from ._protocols import Assertable

__tracebackhide__ = True


class AsserterMixin(Assertable):
    # Todo: Refactor; this isn't good enough!
    # Todo: Theres not good enough reuse with `Asserto` error handling.
    def error(self, reason: str) -> typing.NoReturn:
        # if self._because:
        #     reason = self._because
        # reason = f"[{reason}] {reason}" if self._category else reason
        raise AssertionError(reason)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(actual={self.actual!r})"
