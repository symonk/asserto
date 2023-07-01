from __future__ import annotations

import re

import pytest


def test_raises_without_exception(asserto) -> None:
    asserto(_raiser).should_raise(ValueError).when_called_with(True)


def test_errors_when_no_exc(asserto) -> None:
    with pytest.raises(
        AssertionError,
        match=r"^_raiser did not raise any of \(<class 'ValueError'>, <class 'RuntimeError'>\)\.\s+Instead it raised <class 'AssertionError'> when called with no arguments\.$",  # noqa
    ):
        asserto(_raiser).should_raise((ValueError, RuntimeError)).when_called_with(False)


def test_non_callable_raises_type_error(asserto) -> None:
    with pytest.raises(ValueError, match=r"1 is not callable."):
        asserto(1).should_raise(ValueError).when_called_with(10)


def test_exception_message_mismatch(asserto) -> None:
    asserto(_raiser).should_raise(ValueError, match=r"This is broken\.").when_called_with(True)


def test_no_matching_exc_raises_assertion_error(asserto) -> None:
    def raises():
        raise RuntimeError("test")

    expected = re.escape(
        r"raises did not raise any of (<class 'ZeroDivisionError'>,).  Instead it raised <class 'RuntimeError'> when called with no arguments."  # noqa
    )

    with pytest.raises(AssertionError, match=expected):
        asserto(raises).should_raise(ZeroDivisionError).when_called_with()


def test_no_matching_exc_with_args_and_kwargs(asserto) -> None:
    def raises(x: int, y: str):
        raise ValueError(x, y)

    with pytest.raises(AssertionError, match=r".*when called with \(\(100\,\)\, \{'y': 'foo'\}\)\."):
        asserto(raises).should_raise(ZeroDivisionError).when_called_with(100, y="foo")


def _raiser(x: bool):
    if x:
        raise ValueError("This is broken.")
