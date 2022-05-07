from ._meta import Handler


class StringHandler(Handler):
    """
    A handler responsible for all string based checks.
    """

    def accepts(self, actual: str) -> None:
        """
        Check if this handler can validate the data provided.
        """
        if not isinstance(actual, str):
            raise ValueError(f"{self.__class__} cannot perform checks using: {type(actual)}.  Must be a string.")

    def ends_with(self, actual: str, suffix: str) -> bool:
        """
        Asserts that the value provided begins with the suffix.
        """
        self.accepts(actual)
        return actual.endswith(suffix)

    def starts_with(self, actual: str, prefix: str) -> bool:
        """
        Asserts that the value provided ends with the prefix.
        """
        self.accepts(actual)
        return actual.startswith(prefix)
