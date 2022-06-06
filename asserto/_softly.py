import pprint
import typing


class AssertionErrorContainer:
    """
    An object for storing AssertionError instances when asserto is being used in a soft
    context.  Instances are stored in an underlying sequence and this provides an improved
    API for registering and displaying the errors in a meaningful manner.
    """

    def __init__(self) -> None:
        self.errors: typing.List[AssertionError] = []

    def register_error(self, error: AssertionError) -> None:
        self.errors.append(error)

    def __bool__(self) -> bool:
        """Allow the container to be checked that some errors have occurred."""
        return bool(self.errors)

    def __len__(self) -> int:
        return len(self.errors)

    def clear(self) -> None:
        """Reset all soft failures."""
        self.errors.clear()

    def store(self, error: AssertionError) -> None:
        """Register a new AssertionError."""
        self.errors.append(error)

    def __repr__(self) -> str:
        # Todo: Outline the passes as well as the failures.
        # Todo: Improved tracebacks etc.
        return f"{len(self.errors)} Soft Assertion Failures\n" + pprint.pformat(self.errors, indent=4)
