import pytest
from tests.utility.error_templates import invalid_actual_regex

from asserto import asserto


def test_prefix_not_a_str_type_error() -> None:
    with pytest.raises(TypeError, match="starts_with prefix must be a string, not: <class 'int'>"):
        asserto("foo").starts_with(1)


def test_prefix_with_empty_string_raises_value_error() -> None:
    with pytest.raises(ValueError, match="starts_with cannot be called with an empty prefix string"):
        asserto("foo").starts_with(prefix="")


def test_actual_not_string_or_iterable() -> None:
    with pytest.raises(TypeError, match=invalid_actual_regex(None, str, "starts_with")):
        asserto(None).starts_with("foo")


def test_sucessful_match_on_str() -> None:
    asserto("foo").starts_with("fo")


def test_successful_match_on_iterable() -> None:
    asserto(("f", "o", "o")).starts_with("f")


def test_string_prefix_not_matching() -> None:
    with pytest.raises(AssertionError, match="foo did not begin with prefix='o'"):
        asserto("foo").starts_with("o")


def test_empty_iterable_raises() -> None:
    with pytest.raises(ValueError, match="cannot check if an empty iterable started with foo"):
        asserto({}).starts_with("foo")


def test_iterable_not_starting_with_raises() -> None:
    with pytest.raises(AssertionError, match=r"\['f', 'o', 'o'\] did not start with o"):
        asserto(["f", "o", "o"]).starts_with("o")
