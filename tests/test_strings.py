import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").ends_with("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError, match="Expected `foo` to end with suffix='baz' but it did not."):
        asserto("foo").ends_with("baz")


def test_starts_with_success(asserto) -> None:
    asserto("baz").starts_with("ba")


def test_starts_with_failure(asserto) -> None:
    with pytest.raises(AssertionError, match="baz did not begin with prefix='az'"):
        asserto("baz").starts_with("az")


def test_invalid_type_raises(asserto) -> None:
    with pytest.raises(ValueError, match="`StringHandler` cannot accept type: <class 'int'> when calling: starts_with"):
        asserto(1).starts_with("foo")


def test_is_digit(asserto) -> None:
    asserto("12345").is_digit()


def test_is_alpha(asserto) -> None:
    asserto("abcdef").is_alpha()


def test_iterable_ends_with(asserto) -> None:
    asserto(("foo", "bar", "baz")).ends_with("baz")
    with pytest.raises(AssertionError, match=r"Expected `\('A', 'B', 'C'\)` to end with suffix='B' but it did not\."):
        asserto(("A", "B", "C")).ends_with("B")