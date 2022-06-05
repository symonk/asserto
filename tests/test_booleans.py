import pytest

__tracebackhide__ = True


def test_bool_not_bool_works_successfully(asserto) -> None:
    asserto(True).is_true()
    asserto(False).is_false()
    asserto([]).is_false()
    asserto(()).is_false()
    asserto(0).is_false()
    asserto((1, 2, 3)).is_true()
    asserto(dict(a=1)).is_true()
    asserto({}).is_false()


def test_non_false_raises_for_is_false(asserto) -> None:
    with pytest.raises(AssertionError, match=r"True was not False"):
        asserto(True).is_false()


def test_non_true_raises_for_is_true(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(False).is_true()
    asserto(error.value.args[0]).is_equal_to("False was not True")
