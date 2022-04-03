def test_asserting_equality(asserto) -> None:
    asserto(10).equals(10)


def test_asserting_identity(asserto) -> None:
    obj = object()
    asserto(obj).has_same_identity_of(obj)


def test_length(asserto) -> None:
    asserto([1, 2, 3]).is_length(3)


def test_is_instance_of(asserto) -> None:
    asserto(25).is_instance_of(int)
