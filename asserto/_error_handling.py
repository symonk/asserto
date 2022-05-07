import typing

from ._messaging import FailureCompilation
from ._protocols import IErrorTemplate


class ErrorHandler:
    """
    Core error handler.  Has capabilities to track failures if used in a
    python context or otherwise enforce an AssertionError when conditions
    are not met.
    """

    def __init__(self, reasonable: IErrorTemplate):
        self.reasonable = reasonable
        self.soft_context = False
        self.soft_fails: typing.Optional[FailureCompilation] = None

    def error(self, reason: str) -> None:
        """
        Raise the AssertionError or build on the list of soft assertions which
        will be automatically raised when the context exits.
        """
        error = AssertionError(self.reasonable.format(reason))
        if self.soft_context:
            self.soft_fails.register_error(error)
            return
        raise error from None

    def transition_to_soft(self) -> None:
        """
        Convert the instance into `soft` mode.
        """
        self.soft_context = True
        self.soft_fails = FailureCompilation()

    def transition_to_hard(self) -> None:
        """
        Convert the instance into `hard` mode.
        """
        self.soft_context = False
        self.soft_fails = None
