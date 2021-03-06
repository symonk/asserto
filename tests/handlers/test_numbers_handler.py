import re

import pytest

from asserto import HandlerTypeError


@pytest.mark.parametrize("objtype", ("one", None, True))
def test_handler_only_permits_numbers(asserto, objtype):
    with pytest.raises(HandlerTypeError, match=r"`NumberHandler` cannot accept type: <class.*> when calling: is_zero"):
        asserto(objtype).is_zero()


@pytest.mark.parametrize(
    "number",
    (
        1.25,
        -2.5,
        0.001,
    ),
)
def test_is_zero_success(asserto, number):
    with pytest.raises(AssertionError, match=rf"Expected {re.escape(str(number))} to be 0 but it was not."):
        asserto(number).is_zero()


@pytest.mark.parametrize("number", (0, 0.0, -0, 0j))
def test_is_zero_failure(asserto, number):
    asserto(number).is_zero()


@pytest.mark.parametrize("number", (1, 2.5, -3.5, 4.9j))
def test_is_not_zero_success(asserto, number):
    asserto(number).is_not_zero()


@pytest.mark.parametrize(
    "number",
    (0, 0.0, -0.0, 0j),
)
def test_is_not_zero_failure(asserto, number):
    with pytest.raises(AssertionError, match=rf"Expected {re.escape(str(number))} to not be 0 but it was."):
        asserto(number).is_not_zero()


def test_greater_than_success(asserto):
    asserto(1).is_greater_than(0)


def test_greater_than_failure(asserto):
    with pytest.raises(AssertionError, match="Expected 1 to be greater than 2, but it was not."):
        asserto(1).is_greater_than(2)


def test_lesser_than_success(asserto):
    asserto(100).is_lesser_than(150)


def test_lesser_than_failure(asserto):
    with pytest.raises(AssertionError, match=r"Expected 10 to be lesser than 2, but it was not."):
        asserto(10).is_lesser_than(2)


def test_is_positive_success(asserto):
    asserto(1).is_positive()


@pytest.mark.parametrize("x", (-1, 0))
def test_is_positive_failure(x, asserto):
    with pytest.raises(AssertionError, match=fr"Expected {x} to be greater than 0, but it was not."):
        asserto(x).is_positive()


def test_is_negative_success(asserto):
    asserto(-1).is_negative()


@pytest.mark.parametrize("x", (1, 0))
def test_is_negative_failure(x, asserto):
    with pytest.raises(AssertionError, match=fr"Expected {x} to be lesser than 0, but it was not."):
        asserto(x).is_negative()
