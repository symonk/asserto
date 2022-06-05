import pytest

__tracebackhide__ = True


def test_bool_not_bool_works_successfully(asserto) -> None:
    asserto(True).is_true()
    asserto(False).is_false()
    asserto([]).is_false()
    asserto(()).is_false()
    asserto(0).is_false()
    asserto((1, 2, 3)).is_true()
    asserto(dict(a=1)).is_true()
    asserto({}).is_false()


def test_non_false_raises_for_is_false(asserto) -> None:
    with pytest.raises(AssertionError, match=r"True was not False"):
        asserto(True).is_false()


def test_non_true_raises_for_is_true(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(False).is_true()
    asserto(error.value.args[0]).is_equal_to("False was not True")


def test_truthy_is_true(asserto) -> None:
    class C: ...
    asserto([1]).is_truthy()
    asserto(C()).is_truthy()
    asserto(dict(a=1)).is_truthy()
    asserto(1).is_truthy()


def test_falsy_is_false(asserto) -> None:
    class C:
        def __bool__(self):
            return False

    class D:
        def __len__(self):
            return 0

    asserto({}).is_falsy()
    asserto([]).is_falsy()
    asserto(C()).is_falsy()
    asserto(0).is_falsy()
    asserto(D()).is_falsy()
