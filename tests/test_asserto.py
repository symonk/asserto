import pytest

from asserto import NoAssertAttemptedWarning
from asserto import asserto


def test_simple_repr() -> None:
    asserto(repr(asserto("foo").set_category("n"))).is_equal_to("Asserto(value=foo, category=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, category=None)")


def test_soft_raises_on_exit() -> None:
    with pytest.raises(AssertionError, match="1 Soft Assertion Failures\n.*"):
        with asserto(1) as soft:
            soft.is_equal_to(2)


@pytest.mark.skip(reason="not implemented yet!")
def test_category_is_set() -> None:
    try:
        asserto(1).set_category("Category1").is_false()
    except AssertionError as e:
        asserto(str(e)).is_equal_to("no")


def test_triggered() -> None:
    x = asserto(50)
    asserto(x._triggered).is_false()
    x.is_equal_to(50)
    asserto(x._triggered).is_true()


def test_context_triggered_warning() -> None:
    with pytest.warns(NoAssertAttemptedWarning, match="Asserto instance was created and never used"):
        with asserto(100, warn_unused=True) as _:
            pass


def test_can_be_reassigned() -> None:
    with asserto(100) as a:
        a.is_equal_to(100)
        a.actual = 200
        a.is_equal_to(200)
