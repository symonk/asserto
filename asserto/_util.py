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
