import abc


class ValidateString:
    @abc.abstractmethod
    def ends_with(self, suffix: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def starts_with(self, prefix: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def is_digit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def is_alpha(self) -> None:
        raise NotImplementedError
