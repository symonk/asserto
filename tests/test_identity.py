import pytest

from asserto import asserto


def test_identity_functions_correctly() -> None:
    one = two = three = four = object()
    asserto(one).has_same_identity_as(two).has_same_identity_as(three).has_same_identity_as(four)
    asserto(object()).does_not_have_same_identity_as(object())


def test_identity_fails_when_expected() -> None:
    one, two = object(), object()
    with pytest.raises(AssertionError) as error:
        asserto(one).has_same_identity_as(two)
    asserto(error.value.args[0]).match(r".*does not share identity with:.*")


def test_not_identity_fails_when_expected() -> None:
    x = object()
    with pytest.raises(AssertionError) as error:
        asserto(x).does_not_have_same_identity_as(x)
    asserto(error.value.args[0]).match(r".*shares identity with:.*")
