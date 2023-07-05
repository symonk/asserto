import pytest


def test_description_takes_precedence() -> None:
    with pytest.raises(AssertionError, match="foo!"):
        asserto(100).described_as("foo!").is_equal_to(99)
