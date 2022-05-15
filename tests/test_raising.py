from __future__ import annotations

import pytest

from .markers import NO_UNTRIGGERED_WARNINGS


def test_raises_without_exception(asserto) -> None:
    asserto(_raiser).should_raise(ValueError).when_called_with(x=True)


@NO_UNTRIGGERED_WARNINGS
def test_errors_when_no_exc(asserto) -> None:
    with pytest.raises(AssertionError, match=r"^<function _raiser at .*> never raised any of: \(<class 'ValueError'>, <class 'RuntimeError'>\)$"):
        asserto(_raiser).should_raise((ValueError, RuntimeError)).when_called_with(x=False)


def test_non_callable_raises_type_error(asserto) -> None:
    with pytest.raises(ValueError, match=r"1 is not callable."):
        asserto(1).should_raise(Exception).when_called_with(10)


def _raiser(x: bool):
    if x:
        raise ValueError("foo!")
