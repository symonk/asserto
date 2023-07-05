import re

import pytest

from asserto import UnsupportedHandlerTypeError
from asserto import asserto


@pytest.mark.parametrize("objtype", ("one", None, True))
def test_handler_only_permits_numbers(objtype) -> None:
    with pytest.raises(
        UnsupportedHandlerTypeError, match=r"`NumberHandler` cannot accept type: <class.*> when calling: is_zero"
    ):
        asserto(objtype).is_zero()


@pytest.mark.parametrize(
    "number",
    (
        1.25,
        -2.5,
        0.001,
    ),
)
def test_is_zero_success(number) -> None:
    with pytest.raises(AssertionError, match=rf"Expected {re.escape(str(number))} to be 0 but it was not."):
        asserto(number).is_zero()


@pytest.mark.parametrize("number", (0, 0.0, -0, 0j))
def test_is_zero_failure(number) -> None:
    asserto(number).is_zero()


@pytest.mark.parametrize("number", (1, 2.5, -3.5, 4.9j))
def test_is_not_zero_success(number) -> None:
    asserto(number).is_not_zero()


@pytest.mark.parametrize(
    "number",
    (0, 0.0, -0.0, 0j),
)
def test_is_not_zero_failure(number) -> None:
    with pytest.raises(AssertionError, match=rf"Expected {re.escape(str(number))} to not be 0 but it was."):
        asserto(number).is_not_zero()


def test_greater_than_success() -> None:
    asserto(1).is_greater_than(0)


def test_greater_than_failure() -> None:
    with pytest.raises(AssertionError, match="Expected 1 to be greater than 2, but it was not."):
        asserto(1).is_greater_than(2)


def test_lesser_than_success() -> None:
    asserto(100).is_lesser_than(150)


def test_lesser_than_failure() -> None:
    with pytest.raises(AssertionError, match=r"Expected 10 to be lesser than 2, but it was not."):
        asserto(10).is_lesser_than(2)


def test_is_positive_success() -> None:
    asserto(1).is_positive()


@pytest.mark.parametrize("x", (-1, 0))
def test_is_positive_failure(
    x,
) -> None:
    with pytest.raises(AssertionError, match=rf"Expected {x} to be greater than 0, but it was not."):
        asserto(x).is_positive()


def test_is_negative_success() -> None:
    asserto(-1).is_negative()


@pytest.mark.parametrize("x", (1, 0))
def test_is_negative_failure(
    x,
) -> None:
    with pytest.raises(AssertionError, match=rf"Expected {x} to be lesser than 0, but it was not."):
        asserto(x).is_negative()


def test_is_between_not_between_happy_path() -> None:
    asserto(100).is_between(100, 101, inclusive=True)
    asserto(5).is_between(4, 6)
    asserto(5).is_not_between(6, 10)
    asserto(5).is_not_between(5, 8, inclusive=True)


def test_is_between_fails_correctly() -> None:
    with pytest.raises(AssertionError, match=re.escape(r"Expected 100 to be between (200, ..., 500)")):
        asserto(100).is_between(200, 500)


def test_is_not_between_fails_correctly() -> None:
    with pytest.raises(AssertionError, match=re.escape(r"Expected 250 to not be between (200, ..., 500)")):
        asserto(250).is_not_between(200, 500)


def test_more_than_less_than() -> None:
    asserto(1).is_less_than(2)
    asserto(5).is_more_than(3)
