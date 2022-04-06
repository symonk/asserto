import pytest


def test_identity_functions_correctly(asserto) -> None:
    one = two = three = four = object()
    asserto(one).refers_to(two).refers_to(three).refers_to(four)
    asserto(object()).does_not_refer_to(object())


def test_identity_fails_when_expected(asserto) -> None:
    one, two = object(), object()
    with pytest.raises(AssertionError) as error:
        asserto(one).refers_to(two)
    asserto(error.value.args[0]).matches(r"^<object object at.*is not: <object object at.*>")
