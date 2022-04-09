from __future__ import annotations


class State:
    """
    A state context. Various flags for asserto instances that later drive behaviour.
    """

    def __init__(self) -> None:
        self.soft_mode = False
        self.warning_mode = False
        self.triggered = False
        self.context = False
        self.descriptive = None
