import re

import pytest

from asserto import asserto
from asserto._exceptions import ActualTypeError  # noqa

from .utility.length import DunderLen


def test_length() -> None:
    asserto([1, 2, 3]).has_length(3)
    asserto(DunderLen(2)).has_length(2)
    asserto([]).has_length(0)


def test_length_mismatch() -> None:
    with pytest.raises(AssertionError, match=re.escape("Length of: (1, 2, 3) was not equal to: 4")):
        asserto((1, 2, 3)).has_length(4)


def test_length_fails() -> None:
    with pytest.raises(AssertionError, match=re.escape("Length of: DunderLen(x=100) was not equal to: 99")):
        asserto(DunderLen(100)).has_length(99)


def test_length_below_zero() -> None:
    with pytest.raises(ValueError, match="-5 must be an int and greater than 0"):
        asserto(-5).has_length(-5)
