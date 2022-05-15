import re

import pytest


def test_regex_matches(asserto) -> None:
    asserto("Hello World").match(r"^H[a-z]{4}\sW[a-z]{1}")


def test_regex_non_match_raises(asserto) -> None:
    with pytest.raises(AssertionError, match=re.escape("Hello World did not begin with pattern: pattern='^F$'")):
        asserto("Hello World").match(r"^F$")


def test_match(asserto):
    asserto("hello world").match(r"hello")


def test_search(asserto):
    asserto("Hello World").search(r"World")


def test_fullmatch(asserto):
    asserto("Only Full Matches").fullmatch(r"Only Full .*")


def test_findall(asserto):
    asserto("oneoneoneXoneoneone").findall(r"one", count=6)
