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
        self.exc_types: typing.Iterable[BaseException] = to_iterable(exc_types)
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
            _ = self._proxy_val(*args, **kwargs)
            self.asserto_ref.error(f"{self._proxy_val} never raised any of: {self.exc_types}")
        except self.exc_types as e:  # type: ignore[misc]
            if self.pattern is not None and self.pattern.match(str(e)) is None:
                self.asserto_ref.error(
                    f"Exception occurred but did not match pattern: {self.pattern} instead was: {str(e)}"
                )
