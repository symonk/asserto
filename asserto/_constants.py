import dataclasses


@dataclasses.dataclass(frozen=True)
class AssertTypes:
    """
    An encapsulation of assertion types.
        HARD: Instant failure, the default.
        SOFT: A collection of failures, compiled at the end of the test.
    """

    HARD = "hard"
    SOFT = "soft"
