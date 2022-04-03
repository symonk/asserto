import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").ends_with("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError):
        asserto("foo").ends_with("baz")
