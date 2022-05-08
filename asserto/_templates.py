""" Error message templates. """
import string
from dataclasses import dataclass


class CallableTemplate:
    """
    A callable template that delegates to substitute when called.
    """

    def __init__(self, template: str) -> None:
        self.template = string.Template(template)

    def __call__(self, **kwargs):
        return self.template.substitute(**kwargs)


@dataclass(frozen=True)
class StringErrors:
    ends_with: CallableTemplate = CallableTemplate("$actual did not end with $expected")
    starts_with: CallableTemplate = CallableTemplate("$actual did not start with $expected")
    is_alpha: CallableTemplate = CallableTemplate("$actual did not contain only unicode letters")
    is_digit: CallableTemplate = CallableTemplate("$actual did not contain only numeric digits")


class Errors:
    """
    A Facade to access the underlying errors via chained API.
    """

    strings = str = StringErrors
