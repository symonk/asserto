import re
import typing

EXC_TYPES_ALIAS = typing.Union[typing.Type[BaseException], typing.Iterable[typing.Type[BaseException]]]
CALLABLE_ALIAS = typing.Callable[[typing.Any], typing.Any]
RE_FLAGS_ALIAS = typing.Union[int, re.RegexFlag]
RE_PATTERN_ALIAS = typing.Union[str, typing.Pattern[str]]
