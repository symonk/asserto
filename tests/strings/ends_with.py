import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").ends_with("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError, match="Expected `foo` to end with suffix='baz' but it did not."):
        asserto("foo").ends_with("baz")


def test_iterable_ends_with(asserto) -> None:
    asserto(("foo", "bar", "baz")).ends_with("baz")
    with pytest.raises(AssertionError, match=r"Expected `\('A', 'B', 'C'\)` to end with suffix='B' but it did not\."):
        asserto(("A", "B", "C")).ends_with("B")
