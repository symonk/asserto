import typing

T = typing.TypeVar("T")


def to_iterable(item: typing.Union[typing.Iterable[T], T]) -> typing.Tuple[T]:
    """
    Creates a new tuple from any iterable or returns a single item tuple if a single element
    is passed as item.
    :param item: An iterable or single element.
    :return: A tuple of items
    """
    try:
        _iter = iter(item)
        return tuple(_iter)
    except TypeError:
        return (item,)


def is_namedtuple_like(obj: typing.Any) -> bool:
    """
    Check if an object is likely a named tuple
    :param obj:
    :return:
    """
    t = type(obj)
    bases = t.__bases__
    if len(bases) != 1 and bases[0] != tuple:
        return False
    fields = getattr(obj, "_fields", None)
    if not isinstance(fields, tuple):
        return False
    return all(type(f) == str for f in fields)
