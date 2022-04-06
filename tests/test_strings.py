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
