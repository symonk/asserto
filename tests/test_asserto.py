import pytest

from asserto import AssertTypes
from asserto import UntriggeredAssertoWarning

from .markers import NO_UNTRIGGERED_WARNINGS


@NO_UNTRIGGERED_WARNINGS
def test_repr_soft(asserto) -> None:
    asserto(repr(asserto("foo").with_category("n"))).is_equal_to("Asserto(value=foo, type_of=hard, category=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, type_of=hard, category=None)")
    asserto(repr(asserto(100, AssertTypes.SOFT))).is_equal_to("Asserto(value=100, type_of=soft, category=None)")
    asserto(repr(asserto(100, AssertTypes.WARN))).is_equal_to("Asserto(value=100, type_of=warn, category=None)")


@NO_UNTRIGGERED_WARNINGS
def test_soft_context_active(asserto) -> None:
    with asserto(1) as soft:
        asserto(soft._state.context).is_true()
    asserto(soft._state.context).is_false()


@pytest.mark.skip(reason="not implemented yet!")
def test_category_is_set(asserto) -> None:
    try:
        asserto(1).with_category("Category1").is_false()
    except AssertionError as e:
        asserto(str(e)).is_equal_to("no")


def test_triggered(asserto) -> None:
    x = asserto(50)
    asserto(x._state.triggered).is_false()
    x.is_equal_to(50)
    asserto(x._state.triggered).is_true()


@NO_UNTRIGGERED_WARNINGS
def test_context_triggered_warning(asserto) -> None:
    with pytest.warns(UntriggeredAssertoWarning, match="Asserto instance was created and never used"):
        with asserto(100) as _:
            pass


@NO_UNTRIGGERED_WARNINGS
def test_non_context_triggered_warning(asserto) -> None:
    with pytest.warns(UntriggeredAssertoWarning, match="Asserto instance was created and never used"):
        asserto(100)


# Test invoking description after triggered raises;
