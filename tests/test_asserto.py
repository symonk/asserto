from asserto import AssertTypes


def test_repr_soft(asserto) -> None:
    asserto(repr(asserto("foo", description="n"))).is_equal_to("Asserto(value=foo, type_of=hard, description=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, type_of=hard, description=None)")
    asserto(repr(asserto(100, AssertTypes.SOFT))).is_equal_to("Asserto(value=100, type_of=soft, description=None)")
    asserto(repr(asserto(100, AssertTypes.WARN))).is_equal_to("Asserto(value=100, type_of=warn, description=None)")


def test_soft_context_active(asserto) -> None:
    with asserto(1) as soft:
        asserto(soft._in_context).is_equal_to(True)  # Todo: Refactor `is_true()` when it exists.
    asserto(soft._in_context).is_equal_to(False)  # Todo: Refactor `is_false()` when it exists.
