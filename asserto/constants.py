import dataclasses


@dataclasses.dataclass(frozen=True)
class AssertTypes:
    """
    An encapsulation of assertion types.
        HARD: Instant failure, the default.
        SOFT: A collection of failures, compiled at the end of the test.
        WARN: No failure of the test, omit a warning instead.
    """

    HARD = "hard"
    SOFT = "soft"
    WARN = "warn"
