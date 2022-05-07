from __future__ import annotations

import abc
import typing


class Acceptable:
    """
    Interface for type handlers to verify if they can accept
    the target value or not.  Handlers which cannot accept
    the type should raise a `ValueError` otherwise return
    nothing.
    """

    @abc.abstractmethod
    def accepts(self, actual: typing.Any) -> None:
        raise NotImplementedError


class AcceptsStrings(Acceptable):
    @abc.abstractmethod
    def accepts(self, actual: typing.Any) -> None:
        raise NotImplementedError

    def ends_with(self, actual: typing.Any, suffix: str) -> bool:
        ...

    def starts_with(self, actual: typing.Any, prefix: str) -> bool:
        ...
