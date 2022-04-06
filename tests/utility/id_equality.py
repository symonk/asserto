import typing


class EqualObj:
    def __init__(self, x: int) -> None:
        self.x = x

    def __repr__(self) -> str:
        return f"EqualObj(x={self.x})"

    def __hash__(self) -> int:
        return hash(self.x)

    def __eq__(self, other: typing.Any) -> bool:
        return False if not isinstance(other, EqualObj) else self.x == other.x
