import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").ends_with("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError, match="foo did not end with suffix='baz'"):
        asserto("foo").ends_with("baz")


def test_starts_with_success(asserto) -> None:
    asserto("baz").starts_with("ba")


def test_starts_with_failure(asserto) -> None:
    with pytest.raises(AssertionError, match="baz did not begin with prefix='az'"):
        asserto("baz").starts_with("az")


def test_invalid_type_raises(asserto) -> None:
    with pytest.raises(ValueError, match="function: starts_with does not support type: <class 'int'>"):
        asserto(1).starts_with("foo")


def test_is_digit(asserto) -> None:
    asserto("12345").is_digit()


def test_is_alpha(asserto) -> None:
    asserto("abcdef").is_alpha()
