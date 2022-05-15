import re
import typing

IS_INSTANCE_ALIAS = typing.Union[typing.Type[typing.Any]]
EXC_TYPES_ALIAS = typing.Union[typing.Type[BaseException], typing.Iterable[BaseException]]
CALLABLE_ALIAS = typing.Callable[[typing.Any], typing.Any]
RE_FLAGS_ALIAS = typing.Union[int, re.RegexFlag]
RE_PATTERN_ALIAS = typing.Union[str, typing.Pattern[str]]
