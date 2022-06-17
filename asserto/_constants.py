import dataclasses


@dataclasses.dataclass(frozen=True)
class Methods:
    """
    Encapsulation of method names.  These are used as part of the dynamic dispatch
    to various handlers responsible for individual assertion methods.
    """

    # -- Strings

    ENDS_WITH: str = "ends_with"
    STARTS_WITH: str = "starts_with"
    IS_DIGIT: str = "is_digit"
    IS_ALPHA: str = "is_alpha"

    # -- Regular Expressions

    MATCH: str = "match"
    SEARCH: str = "search"
    FULLMATCH: str = "fullmatch"
    FINDALL: str = "findall"

    # -- Base Objects

    IS_TRUE: str = "is_true"
    IS_TRUTHY: str = "is_truthy"
    IS_FALSE: str = "is_false"
    IS_FALSY: str = "is_falsy"
    IS_EQUAL_TO: str = "is_equal_to"
    IS_NOT_EQUAL_TO: str = "is_not_equal_to"
    HAS_LENGTH: str = "has_length"
    IS_INSTANCE: str = "is_instance"
    HAS_SAME_IDENTITY_AS: str = "has_same_identity_as"
    DOES_NOT_HAVE_SAME_IDENTITY_AS: str = "does_not_have_same_identity_as"
    IS_NONE: str = "is_none"
    IS_NOT_NONE: str = "is_not_none"

    # -- Numeric
    IS_ZERO: str = "is_zero"
    IS_NOT_ZERO: str = "is_not_zero"
    IS_GREATER_THAN: str = "is_greater_than"
    IS_LESSER_THAN: str = "is_lesser_than"
    IS_POSITIVE: str = "is_positive"
    IS_NEGATIVE: str = "is_negative"
