import re

import pytest


def test_regex_matches(asserto) -> None:
    asserto("Hello World").match(r"^H[a-z]{4}\sW[a-z]{1}")


def test_regex_non_match_raises(asserto) -> None:
    with pytest.raises(AssertionError, match=re.escape("Hello World did not begin with pattern: pattern='^F$'")):
        asserto("Hello World").match(r"^F$")


@pytest.mark.parametrize("actual", [None, 1, Exception])
def test_regex_handler_validator(actual, asserto) -> None:
    with pytest.raises(ValueError, match="function: match does not support type: .*"):
        asserto(None).match(r"")


def test_match(asserto):
    asserto("hello world").match(r"hello")


def test_match_fail(asserto):
    with pytest.raises(AssertionError, match="hello world did not begin with pattern: pattern='ello world'"):
        asserto("hello world").match(r"ello world")


def test_search(asserto):
    asserto("Hello World").search(r"World")


def test_search_fail(asserto):
    with pytest.raises(AssertionError, match="hello world did not contain any matches for: pattern='hello world1'"):
        asserto("hello world").search("hello world1")


def test_fullmatch(asserto):
    asserto("Only Full Matches").fullmatch(r"Only Full .*")


def test_fullmatch_fail(asserto):
    with pytest.raises(AssertionError, match="hello world was not matched entirely by: pattern='hello worl'"):
        asserto("hello world").fullmatch(r"hello worl")


def test_findall(asserto):
    asserto("oneoneoneXoneoneone").findall(r"one", count=6)


def test_findall_fail(asserto):
    with pytest.raises(
        AssertionError, match="helloworldhello had: 2 non overlapping occurrences for pattern: hello, not: 3"
    ):
        asserto("helloworldhello").findall(r"hello", count=3)
