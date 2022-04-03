import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").endswith("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError):
        asserto("foo").endswith("baz")
