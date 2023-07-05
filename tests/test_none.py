import pytest

from asserto import asserto


def test_is_none_or_not_none_works_successfully() -> None:
    asserto(None).is_none()
    asserto(object()).is_not_none()


def test_is_none_incorrect_raises() -> None:
    with pytest.raises(AssertionError, match="1 is not None"):
        asserto(1).is_none()


def test_is_not_none_incorrect_raises() -> None:
    with pytest.raises(AssertionError, match="None is None"):
        asserto(None).is_not_none()
