import typing

from ._asserto import Asserto
from ._constants import AssertTypes


def asserto(actual: typing.Any, type_of: str = AssertTypes.HARD) -> Asserto:
    """
    Retrieve an appropriate asserter for the type of value.
    :param actual: The value to compare against later and defer a type specific asserter from.
    :param type_of: ...
    :return: An instance of an asserter
    """
    return Asserto(actual, type_of)
