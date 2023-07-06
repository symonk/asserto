import pytest
from utility.error_templates import invalid_actual_regex

from asserto import asserto


def test_is_alphabetic_correctly() -> None:
    asserto("abcdef").is_alpha()


def test_is_alphabetic_raises_type_error_when_actual_is_not_a_string() -> None:
    with pytest.raises(TypeError, match=invalid_actual_regex(None, str, "is_alpha")):
        asserto(None).is_alpha()


def test_is_alphabetic_failure() -> None:
    with pytest.raises(AssertionError, match=".* is not alphabetic."):
        asserto("abc1").is_alpha()
