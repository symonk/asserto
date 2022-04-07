import pytest


def test_is_none_or_not_none_works_successfully(asserto) -> None:
    asserto(None).is_none()
    asserto(object()).is_not_none()


def test_is_none_incorrect_raises(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(1).is_none()
    asserto(error.value.args[0]).is_equal_to("1 is not None")


def test_is_not_none_incorrect_raises(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(None).is_not_none()
    asserto(error.value.args[0]).is_equal_to("None is None")
