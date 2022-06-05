import typing

T = typing.TypeVar("T")


def to_iterable(item: typing.Any) -> typing.Tuple[T, ...]:
    """
    Converts a tuple from any items that can be iterated over.
    :param item: Anything, if iterable is concerted to tuple otherwise is a single element tuple of T.
    :return: A tuple of items
    """
    try:
        return tuple(iter(item))
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
