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
        self.soft_fail_compiler: typing.Optional[FailureCompilation] = None

    @property
    def soft_errors(self) -> typing.List[AssertionError]:
        if not self.soft_context or self.soft_fail_compiler is None:
            raise ValueError("Cannot access soft errors outside of a soft context.")
        return self.soft_fail_compiler.errors

    def error(self, cause: typing.Union[AssertionError, str]) -> None:
        """
        Raise the AssertionError or build on the list of soft assertions which
        will be automatically raised when the context exits.  Error can except
        an Assertion error or a string used as message for a newly created one.
        """
        error = cause if not isinstance(cause, str) else AssertionError(self.reasonable.format(cause))
        if self.soft_context and self.soft_fail_compiler is not None:
            # Asserto is being used in a soft fail context.
            self.soft_fail_compiler.register_error(error)
            return
        raise error from None

    def transition_to_soft(self) -> None:
        """
        Convert the instance into `soft` mode.
        """
        self.soft_context = True
        self.soft_fail_compiler = FailureCompilation()

    def transition_to_hard(self) -> None:
        """
        Convert the instance into `hard` mode.
        """
        self.soft_context = False
        self.soft_fail_compiler = None
