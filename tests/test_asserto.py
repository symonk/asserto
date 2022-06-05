import pytest

from asserto import NoAssertAttemptedWarning


def test_simple_repr(asserto) -> None:
    asserto(repr(asserto("foo").set_category("n"))).is_equal_to("Asserto(value=foo, category=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, category=None)")


def test_soft_context_active(asserto) -> None:
    with asserto(1) as soft:
        asserto(soft._error_handler.soft_context).is_true()
    asserto(soft._error_handler.soft_context).is_false()


@pytest.mark.skip(reason="not implemented yet!")
def test_category_is_set(asserto) -> None:
    try:
        asserto(1).set_category("Category1").is_false()
    except AssertionError as e:
        asserto(str(e)).is_equal_to("no")


def test_triggered(asserto) -> None:
    x = asserto(50)
    asserto(x.triggered).is_false()
    x.is_equal_to(50)
    asserto(x.triggered).is_true()


def test_context_triggered_warning(asserto) -> None:
    with pytest.warns(NoAssertAttemptedWarning, match="Asserto instance was created and never used"):
        with asserto(100, warn_unused=True) as _:
            pass
