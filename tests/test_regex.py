import pytest


def test_regex_matches(asserto) -> None:
    asserto("Hello World").matches(r"^H[a-z]{4}\sW[a-z]{4}$")


def test_regex_non_match_raises(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto("Hello World").matches(r"^F$")
    asserto(error.value.args[0]).is_equal_to("^F$ did not match the value: Hello World")
