""" Error message templates. """
from dataclasses import dataclass


@dataclass(frozen=True)
class StringErrors:
    ends_with: str = "{} did not end with {}"
    starts_with: str = "{} did not start with {}"
