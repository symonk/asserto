from collections import namedtuple

from asserto import asserto
from asserto._util import is_iterable
from asserto._util import is_namedtuple_like
from asserto._util import to_iterable


def test_single_item_is_tuple() -> None:
    asserto(to_iterable(1)).is_equal_to((1,))


def test_iterable_is_tuple() -> None:
    asserto(to_iterable([1, 2, 3])).is_equal_to((1, 2, 3))


def test_namedtuple_types() -> None:
    t = namedtuple("t", "a b c")

    class C:
        ...

    asserto(is_namedtuple_like({})).is_false()
    asserto(is_namedtuple_like((1, 2, 3))).is_false()
    asserto(is_namedtuple_like(C())).is_false()
    asserto(is_namedtuple_like(C)).is_false()
    asserto(is_namedtuple_like(None)).is_false()
    asserto(is_namedtuple_like(t(1, 2, 3))).is_true()


class OldSchool:
    def __init__(self) -> None:
        self.x = tuple(range(3))

    def __getitem__(self, x):
        if x > len(self.x):
            raise IndexError
        return self.x[x]


def test_is_iterable() -> None:
    asserto(is_iterable(100)).is_false()
    asserto(is_iterable("foo")).is_true()
    asserto(is_iterable((1, 2, 3))).is_true()
    asserto(is_iterable(OldSchool())).is_true()
