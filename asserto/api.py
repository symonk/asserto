import typing

from .asserto import Asserto


def assert_that(value: typing.Any) -> Asserto:
    """
    Retrieve an appropriate asserter for the type of value.
    :param value: The value to compare against later and defer a type specific asserter from.
    :return: An instance of an asserter
    """
    return Asserto(value)
