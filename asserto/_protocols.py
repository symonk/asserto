from __future__ import annotations

import abc
import typing


class Assertable(typing.Protocol):
    @abc.abstractmethod
    def error(self, reason: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def transition_to_soft(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def transition_to_hard(self) -> None:
        raise NotImplementedError


class IErrorTemplate(typing.Protocol):
    @abc.abstractmethod
    def format(self, reason: str) -> str:
        raise NotImplementedError
