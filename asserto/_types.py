import typing

IS_INSTANCE_ALIAS = typing.Union[typing.Type]
EXC_TYPES_ALIAS = typing.Union[typing.Type[BaseException], typing.Iterable[BaseException]]
CALLABLE_ALIAS = typing.Callable[[typing.Any, ...], typing.Any]
