import typing

from ._asserto import Asserto


def asserto(actual: typing.Any) -> Asserto:
    """
    Retrieve an appropriate asserter for the type of value.
    :param actual: The value to compare against later and defer a type specific asserter from.
    :return: An instance of an asserter
    """
    return Asserto(actual)
