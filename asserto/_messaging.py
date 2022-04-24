import pprint
import typing

from ._protocols import Reasonable


class ComposedFailure:
    """
    Capture multiple assertion failures when used in a soft context mode.
    """

    def __init__(self) -> None:
        self.errors: typing.List[AssertionError] = []

    def register_error(self, error: AssertionError) -> None:
        self.errors.append(error)

    def __bool__(self) -> bool:
        return bool(self.errors)

    def __repr__(self) -> str:
        # Todo: Outline the passes as well as the failures.
        # Todo: Improved tracebacks etc.
        return f"{len(self.errors)} Soft Assertion Failures\n" + pprint.pformat(self.errors, indent=4)


class Reason(Reasonable):
    """
    An encapsulation of assertion error messages.
    """

    def __init__(self, category: typing.Optional[str] = None, description: typing.Optional[str] = None) -> None:
        self.category = category
        self.description = description

    def format(self, reason: str) -> str:
        reason = self.description or reason
        if self.category:
            return f"[{self.category}] {reason}"
        return reason
