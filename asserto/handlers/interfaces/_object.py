import typing

from ._checkable import AcceptsType


class ValidatesBaseTypes(AcceptsType):
    """Todo: Implement"""

    def check_value(self, actual: typing.Any) -> None:
        pass
