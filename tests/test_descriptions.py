import pytest


def test_description_takes_precedence(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(100).described_as("foo!").is_equal_to(99)
    asserto(error.value.args[0]).is_equal_to("foo!")
