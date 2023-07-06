import pytest
from utility.error_templates import invalid_actual_regex

from asserto import asserto


def test_is_digit_success() -> None:
    asserto("111").is_digit()


def test_is_digit_failure() -> None:
    with pytest.raises(AssertionError, match="abc is not a digit string."):
        asserto("abc").is_digit()


def test_is_digit_raises_type_error() -> None:
    with pytest.raises(TypeError, match=invalid_actual_regex(1, str, "is_digit")):
        asserto(1).is_digit()
