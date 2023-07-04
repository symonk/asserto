import pytest
from asserto import asserto


def test_starts_with_success() -> None:
    asserto("baz").starts_with("ba")


def test_starts_with_failure() -> None:
    with pytest.raises(AssertionError, match="baz did not begin with prefix='az'"):
        asserto("baz").starts_with("az")


def test_invalid_type_raises() -> None:
    with pytest.raises(ValueError, match="`StringHandler` cannot accept type: <class 'int'> when calling: starts_with"):
        asserto(1).starts_with("foo")