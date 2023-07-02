import re
import typing

from ._types import EXC_TYPES_ALIAS
from ._types import RE_PATTERN_ALIAS
from ._util import to_iterable
from .descriptors import EnforcedCallable


class ExceptionChecker:
    """
    Encapsulation of the asserto callable exception handling syntax.
    """

    _proxy_val = EnforcedCallable()

    def __init__(
        self,
        exc_types: EXC_TYPES_ALIAS,
        value: typing.Callable[[typing.Any], typing.Any],
        _referent,
        match: typing.Optional[RE_PATTERN_ALIAS] = None,
    ) -> None:
        self.exc_types: typing.Iterable[typing.Type[BaseException]] = to_iterable(exc_types)
        self._proxy_val = value
        self.asserto_ref = _referent
        self.pattern: typing.Optional[re.Pattern[str]] = re.compile(match) if isinstance(match, str) else match

    def when_called_with(self, *args, **kwargs) -> None:
        """
        Call the underlying function with the user supplied arguments;  This returns the result
        of the function back to the asserto instance to enforce error handling & assertion errors
        there.

        If reason is provided; asserto will enforce the exception message is explicitly equal to.

        # Todo: In future support a pattern match.
        # Todo: limitations in this API; what if the called arg has a `reason` attribute?
        """
        try:
            # update 'triggered' status to avoid unnecessary warnings
            self.asserto_ref.triggered = True  # type: ignore[attr-defined]
            self._proxy_val(*args, **kwargs)
            # No exception was raised at all; raise an assertion error.
            self.asserto_ref.error(f"{self._proxy_val} never raised any of: {self.exc_types}")
        except BaseException as e:
            exc_type, exc_string = type(e), str(e)
            if isinstance(e, self.exc_types):  # type: ignore [arg-type]
                if self.pattern:
                    if self.pattern.match(exc_string) is None:
                        # Type matched, but the pattern regex did not, raise.
                        self.asserto_ref.error(
                            f"{exc_type} occurred but did not match pattern: {self.pattern} instead was: {exc_string}"
                        )
                # type matched, no expected pattern, it was a success.
                return
            # The exception was not as expected, raise an assertion error against the type.
            arguments = f"{args, kwargs}" if all((args, kwargs)) else "no arguments"
            self.asserto_ref.error(
                f"{self._proxy_val.__name__} did not raise any of {self.exc_types}.  Instead it raised {exc_type} when called with {arguments}."  # noqa
            )
