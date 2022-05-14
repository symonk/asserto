""" Error message templates. """
import string
import typing
from dataclasses import dataclass


class CallableTemplate:
    """
    A callable template that delegates to substitute when called.  When called all
    templates will be passed an $actual and $expected value.
    """

    def __init__(self, template: str) -> None:
        self.template = string.Template(template)

    def __call__(self, actual: typing.Optional[typing.Any] = None, expected: typing.Optional[typing.Any] = None):
        return self.template.substitute(actual=actual, expected=expected)


@dataclass(frozen=True)
class StringErrors:
    """
    These should match the assert function names as dispatch will attempt to resolve
    the correct error message implicitly if one is not explicitly passed and shovel
    actual and expected arguments into it.
    """

    ends_with: CallableTemplate = CallableTemplate("$actual did not end with $expected")
    starts_with: CallableTemplate = CallableTemplate("$actual did not start with $expected")
    is_alpha: CallableTemplate = CallableTemplate("$actual did not contain only unicode letters")
    is_digit: CallableTemplate = CallableTemplate("$actual did not contain only numeric digits")


class Errors:
    """
    A Facade to access the underlying errors via chained API.
    """

    strings = StringErrors
