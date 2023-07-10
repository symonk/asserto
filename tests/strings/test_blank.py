import pytest
from utility.error_templates import invalid_actual_regex

from asserto import asserto


def test_blank_string() -> None:
    asserto("").is_blank()


def test_non_blank_string() -> None:
    with pytest.raises(AssertionError, match="f was not an empty string."):
        asserto("f").is_blank()


def test_non_string_actual_raises() -> None:
    with pytest.raises(TypeError, match=invalid_actual_regex(1, str, "is_blank")):
        asserto(1).is_blank()
