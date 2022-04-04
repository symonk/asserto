def test_asserting_identity(asserto) -> None:
    obj = object()
    asserto(obj).has_same_identity_of(obj)
