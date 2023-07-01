import pytest

from .utility.id_equality import EqualObj


def test_simple_equality_works(asserto) -> None:
    asserto(10).is_equal_to(10)

    
def test_simple_equality_with_equals(asserto) -> None:
    asserto(100).equals(100)


def test_equality_works_as_expected(asserto) -> None:
    asserto(EqualObj(100)).is_equal_to(EqualObj(100))
    asserto(EqualObj(100)).is_not_equal_to(EqualObj(99))


def test_equality_fails_as_expected(asserto) -> None:
    with pytest.raises(AssertionError, match=r"EqualObj\(x=500\) is not equal to: 200"):
        asserto(EqualObj(500)).is_equal_to(200)

        
def test_equals_fail(asserto) -> None:
    with pytest.raises(AssertionError, match=r"100 is not equal to: 200"):
        asserto(100).equals(200)