from .interfaces import ValidatesStringTypes


class StringHandler(ValidatesStringTypes):
    """
    A handler responsible for all string based checks.
    """

    def is_alpha(self, actual: str) -> bool:
        return actual.isalpha()

    def is_digit(self, actual: str) -> bool:
        return actual.isdigit()

    def ends_with(self, actual: str, suffix: str) -> bool:
        return actual.endswith(suffix)

    def starts_with(self, actual: str, prefix: str) -> bool:
        return actual.startswith(prefix)
