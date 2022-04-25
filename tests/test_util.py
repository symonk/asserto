from asserto._util import to_iterable


def test_single_item_is_tuple(asserto) -> None:
    asserto(to_iterable(1)).is_equal_to((1,))


def test_iterable_is_tuple(asserto) -> None:
    asserto(to_iterable([1, 2, 3])).is_equal_to((1, 2, 3))
