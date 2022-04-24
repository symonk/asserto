from __future__ import annotations


class State:
    """
    A state context. Various flags for asserto instances that later drive behaviour.
    """

    def __init__(self) -> None:
        self.context = False
