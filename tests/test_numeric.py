import re

import pytest

from asserto import InvalidHandlerTypeException


def test_invalid_types(asserto):
    with pytest.raises(
        InvalidHandlerTypeException, match="`NumericHandler` cannot accept type: <class 'str'> when calling: is_zero"
    ):
        asserto("foo").is_zero()


@pytest.mark.parametrize(
    "number",
    (
        1.25,
        -2.5,
        0.001,
    ),
)
def test_is_zero_success(asserto, number):
    with pytest.raises(AssertionError, match=rf"{re.escape(str(number))} was not equal to 0"):
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
    with pytest.raises(AssertionError, match=rf"{re.escape(str(number))} was 0"):
        asserto(number).is_not_zero()


def test_greater_than_success(asserto):
    asserto(1).is_greater_than(0)


def test_greater_than_failure(asserto):
    with pytest.raises(AssertionError, match="1 was less than 2"):
        asserto(1).is_greater_than(2)
