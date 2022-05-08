import pytest


def test_ends_with_success(asserto) -> None:
    asserto("foo").ends_with("oo")


def test_ends_with_failures(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto("foo").ends_with("baz")
    asserto(error.value.args[0]).is_equal_to("foo did not end with baz")


def test_starts_with_success(asserto) -> None:
    asserto("baz").starts_with("ba")


def test_starts_with_failure(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto("baz").starts_with("az")
    asserto(error.value.args[0]).is_equal_to("baz did not start with az")


def test_invalid_type_raises(asserto) -> None:
    with pytest.raises(ValueError) as error:
        asserto(1).starts_with("foo")
    asserto(error.value.args[0]).is_equal_to(
        "'StringHandler' cannot perform checks using: <class 'int'>.  Must be a string."
    )


def test_is_digit(asserto) -> None:
    asserto("12345").is_digit()


def test_is_alpha(asserto) -> None:
    asserto("abcdef").is_alpha()
