class DunderLen:
    def __init__(self, x: int) -> None:
        self.x = x

    def __repr__(self) -> str:
        return f"DunderLen(x={self.x})"

    def __len__(self) -> int:
        return self.x
