import typing


class AcceptsType(typing.Protocol):
    """
    Implicit interface for various handler types that guarantees they can support the
    type of value that was passed to them.
    """

    def check_value(self) -> None:
        ...
