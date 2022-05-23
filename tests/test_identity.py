import pytest


def test_identity_functions_correctly(asserto) -> None:
    one = two = three = four = object()
    asserto(one).has_same_identity_as(two).has_same_identity_as(three).has_same_identity_as(four)
    asserto(object()).does_not_have_same_identity_as(object())


def test_identity_fails_when_expected(asserto) -> None:
    one, two = object(), object()
    with pytest.raises(AssertionError) as error:
        asserto(one).has_same_identity_as(two)
    asserto(error.value.args[0]).match(r"^<object object at.*is not: <object object at.*>")


def test_not_identity_fails_when_expected(asserto) -> None:
    x = object()
    with pytest.raises(AssertionError) as error:
        asserto(x).does_not_have_same_identity_as(x)
    asserto(error.value.args[0]).match(".*points to the same memory location as.*")
