import pytest

from asserto._exceptions import ActualTypeError  # noqa

from .utility.length import DunderLen


def test_length(asserto) -> None:
    asserto([1, 2, 3]).has_length(3)
    asserto(DunderLen(2)).has_length(2)
    asserto([]).has_length(0)


def test_length_mismatch(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto((1, 2, 3)).has_length(4)
    asserto(error.value.args[0]).is_equal_to("Length of: (1, 2, 3) was not equal to: 4")


def test_length_fails(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(DunderLen(100)).has_length(99)
    asserto(error.value.args[0]).is_equal_to("Length of: DunderLen(x=100) was not equal to: 99")
