import pytest

from asserto import asserto


def test_is_digit_success() -> None:
    asserto("111").is_digit()


def test_is_digit_failure() -> None:
    with pytest.raises(AssertionError, match="abc is not a digit string."):
        asserto("abc").is_digit()


def test_is_digit_raises_type_error() -> None:
    with pytest.raises(TypeError, match="1 is not a string, it is of type: <class 'int'>."):
        asserto(1).is_digit()
