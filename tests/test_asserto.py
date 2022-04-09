import pytest

from asserto import AssertTypes


def test_repr_soft(asserto) -> None:
    asserto(repr(asserto("foo", category="n"))).is_equal_to("Asserto(value=foo, type_of=hard, category=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, type_of=hard, category=None)")
    asserto(repr(asserto(100, AssertTypes.SOFT))).is_equal_to("Asserto(value=100, type_of=soft, category=None)")
    asserto(repr(asserto(100, AssertTypes.WARN))).is_equal_to("Asserto(value=100, type_of=warn, category=None)")


def test_soft_context_active(asserto) -> None:
    with asserto(1) as soft:
        asserto(soft._state.context).is_true()
    asserto(soft._state.context).is_false()


@pytest.mark.skip(reason="not implemented yet!")
def test_category_is_set(asserto) -> None:
    try:
        asserto(1).grouped_by("Category1").is_false()
    except AssertionError as e:
        asserto(str(e)).is_equal_to("no")


def test_triggered(asserto) -> None:
    x = asserto(50)
    asserto(x._state.triggered).is_false()
    x.is_equal_to(50)
    asserto(x._state.triggered).is_true()


# Test invoking description after triggered raises;
# Test not invoking any assertions warns
