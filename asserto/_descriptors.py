import typing
from abc import ABC
from abc import abstractmethod


class Validatable(ABC):
    """
    Base class for custom validation descriptors.
    """

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, owner):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value: typing.Any) -> None:
        raise NotImplementedError


class IsCallable(Validatable):
    # Todo: handle `update_triggered` here; its omitting warnings.
    def validate(self, value: typing.Any) -> None:
        if not callable(value):
            raise ValueError(f"{value} was not callable; it must be a callable type.")
