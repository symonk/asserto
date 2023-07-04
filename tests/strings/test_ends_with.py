import pytest

from asserto import assert_that


def test_ends_with_success() -> None:
    assert_that("foo").ends_with("oo")


def test_ends_with_failures() -> None:
    with pytest.raises(AssertionError, match="Expected `foo` to end with suffix='baz' but it did not."):
        assert_that("foo").ends_with("baz")


def test_iterable_ends_with() -> None:
    assert_that(("foo", "bar", "baz")).ends_with("baz")
    with pytest.raises(AssertionError, match=r"Expected `\('A', 'B', 'C'\)` to end with suffix='B' but it did not\."):
        assert_that(("A", "B", "C")).ends_with("B")
