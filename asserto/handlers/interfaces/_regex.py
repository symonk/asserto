import abc
import re
import typing


class ValidateRegex:
    @abc.abstractmethod
    def matches_beginning(self, expected: typing.Any, flags: typing.Union[int, re.RegexFlag] = 0) -> bool:
        raise NotImplementedError
