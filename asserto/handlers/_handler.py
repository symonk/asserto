import typing


class Handler:
    """
    Useful utility functions for handlers.  Subclasses of handlers should raise
    AssertionErrors when things are wrong; the asserto machinery is catching them
    internally to wrap and bubble something more user-friendly back to the user.
    """

    def __init__(self, actual: typing.Any) -> None:
        self.actual = actual

    @staticmethod
    def dispatch_and_raise(fn, expected, error, *args, **kwargs):
        """
        Dispatches a call to an underlying callable and if the return value of the function
        is not equal to expected, raises an AssertionError.
        """
        if fn(*args, **kwargs) != expected:
            raise AssertionError(error)

    def raise_if_length_equals(self, length: int = 0) -> typing.Literal[True]:
        """Checks the length of a Sized implementation and raises a ValueError if it is zero.
        Returns `True` if it succeeds to allow chaining of checks in handler subclasses."""
        if len(self.actual) == length:
            raise ValueError(f"{self.actual} is empty.")
        return True
