import abc
import typing


class Validatable(abc.ABC):
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

    @abc.abstractmethod
    def validate(self, value: typing.Any) -> None:
        """Raise a ValueError if validation fails."""
        raise NotImplementedError
