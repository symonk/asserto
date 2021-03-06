from __future__ import annotations

import pytest


def test_raises_without_exception(asserto) -> None:
    asserto(_raiser).should_raise(ValueError).when_called_with(True)


def test_errors_when_no_exc(asserto) -> None:
    with pytest.raises(
        AssertionError,
        match=r"^<function _raiser at .*> never raised any of: \(<class 'ValueError'>, <class 'RuntimeError'>\)$",
    ):
        asserto(_raiser).should_raise((ValueError, RuntimeError)).when_called_with(False)


def test_non_callable_raises_type_error(asserto) -> None:
    with pytest.raises(ValueError, match=r"1 is not callable."):
        asserto(1).should_raise(ValueError).when_called_with(10)


def test_exception_message_mismatch(asserto) -> None:
    asserto(_raiser).should_raise(ValueError, match=r"This is broken\.").when_called_with(True)


def _raiser(x: bool):
    if x:
        raise ValueError("This is broken.")
