import abc

from ._acceptable import Acceptable


class CanValidateStrings(Acceptable):
    def accepts(self, actual: str) -> None:
        """
        Check if this handler can validate the data provided.
        """
        if not isinstance(actual, str):
            raise ValueError(
                f"{repr(self.__class__.__name__)} cannot perform checks using: {type(actual)}.  Must be a string."
            )

    @abc.abstractmethod
    def ends_with(self, actual: str, suffix: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def starts_with(self, actual: str, prefix: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def is_digit(self, actual: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def is_alpha(self, actual: str) -> bool:
        raise NotImplementedError
