import re
from collections import namedtuple
from types import SimpleNamespace

import pytest

from asserto import asserto

from .utility.dynamic import Dynamic


def test_attr_access_works_on_various_types() -> None:
    asserto(Dynamic(a=10, b=20)).a_is(10)  # user class
    asserto({"foo": 10}).foo_is(10)  # dict
    asserto(SimpleNamespace(x=100)).x_is(100)  # alternative mapping
    t = namedtuple("foo", "baz")
    asserto(t(1337)).baz_is(1337)


def test_no_arg_callable_ok() -> None:
    class C:
        def ok(self):
            return 10

    asserto(C()).ok_is(10)


def test_no_arg_callable_not_ok() -> None:
    class C:
        def bound_with_args(self, x):
            return 10

    with pytest.raises(TypeError, match="bound_with_args expects arguments, this is not supported"):
        asserto(C()).bound_with_args_is(10)


def test_no_attr() -> None:
    with pytest.raises(AssertionError, match="{} missing attribute: a"):
        asserto(Dynamic()).a_is(10)


def test_attr_value_wrong() -> None:
    with pytest.raises(AssertionError, match="9 was not equal to: 10"):
        asserto(Dynamic(a=9)).a_is(10)


def test_no_attr_raises_attribute_error() -> None:
    with pytest.raises(AttributeError):
        # dynamic dispatch without ending in `_is`
        asserto(True).not_ends_with(10)


def test_single_argument() -> None:
    with pytest.raises(TypeError, match=re.escape("Dynamic assertion takes 1 argument but 2 was given. (1, 2)")):
        asserto(dict(a=1)).a_is(1, 2)
