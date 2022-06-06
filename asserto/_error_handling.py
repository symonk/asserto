import abc
import typing

from ._softly import AssertionErrorContainer


class RaisesErrors(typing.Protocol):
    @abc.abstractmethod
    def check_should_raise(
        self,
        softly: bool,
        cause: typing.Union[AssertionError, str],
        description: typing.Optional[str] = None,
        category: typing.Optional[str] = None,
    ) -> None:
        """Checks and raises immediately for hard failures when not used in a context"""

    @abc.abstractmethod
    def check_soft_raise(self):
        """Checks and raises for soft failures when exiting the context"""

    @abc.abstractmethod
    def reset(self):
        """Reset the soft context failures."""


class ErrorHandler:
    """
    The Error handler.  Responsible for raising the underlying AssertionError's when things
    are amiss for each individual handler instance.
    """

    def __init__(self):
        self.context_failures = AssertionErrorContainer()

    def reset(self) -> None:
        """Clear the underlying sequence of AssertionError instances."""
        self.context_failures.clear()

    def check_should_raise(
        self,
        softly: bool,
        cause: typing.Union[AssertionError, str],
        description: typing.Optional[str] = None,
        category: typing.Optional[str] = None,
    ) -> None:
        """
        Raise the AssertionError or build on the list of soft assertions which
        will be automatically raised when the context exits.  Error can except
        an Assertion error or a string used as message for a newly created one.
        """
        error = cause if isinstance(cause, AssertionError) else self.build_assertion_error(cause, description, category)
        # Check if in 'soft' mode as in the `Asserto` instance was instantiated as a context manager.
        if softly:
            self.context_failures.store(error)
            return
        raise error from None

    def check_soft_raise(self):
        if self.context_failures:
            # The asserto instance had had some soft assertion failures; raise them now.
            raise AssertionError(repr(self.context_failures)) from None

    @staticmethod
    def build_assertion_error(
        cause: str, description: typing.Optional[str] = None, category: typing.Optional[str] = None
    ) -> AssertionError:
        """
        Generates exception messages for a given failure.
        Resolving an assertion error works as follows:

            :: If a description was provided, it is the main exception message
            :: Otherwise `cause` is used, this is typically populated by Asserto
            :: If a category was provided, it is prefixed to the exception message.

        Description gives the user the chance to interject their own bespoke error message on the assertions.

        :param cause: A string for the error message, is always a string at this point.
        :param description: User defined description to provide a custom message on the AssertionError.
        :param category: A prefix for grouping purposes.
        """
        message = description or cause
        return AssertionError(message if category is None else f"[{category}] {message}")
