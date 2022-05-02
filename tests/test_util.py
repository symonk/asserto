from collections import namedtuple

from asserto._util import is_namedtuple_like
from asserto._util import to_iterable


def test_single_item_is_tuple(asserto) -> None:
    asserto(to_iterable(1)).is_equal_to((1,))


def test_iterable_is_tuple(asserto) -> None:
    asserto(to_iterable([1, 2, 3])).is_equal_to((1, 2, 3))


def test_namedtuple_types(asserto) -> None:
    t = namedtuple("t", "a b c")

    class C:
        ...

    asserto(is_namedtuple_like({})).is_false()
    asserto(is_namedtuple_like((1, 2, 3))).is_false()
    asserto(is_namedtuple_like(C())).is_false()
    asserto(is_namedtuple_like(C)).is_false()
    asserto(is_namedtuple_like(None)).is_false()
    asserto(is_namedtuple_like(t(1, 2, 3))).is_true()
