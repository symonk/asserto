import pytest

from .utility.dynamic import Dynamic


def test_is_attr_works(asserto) -> None:
    asserto(Dynamic(a=10, b=20)).a_is(10)
    # dict not yet supported -> asserto({"A": 1}).has_A(1)


def test_no_attr(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(Dynamic()).a_is(10)
    asserto(error.value.args[0]).is_equal_to("{} did not have an a attribute.")


def test_attr_value_wrong(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(Dynamic(a=9)).a_is(10)
    asserto(error.value.args[0]).is_equal_to("{'a': 9} attribute: a was not equal to: 10")
