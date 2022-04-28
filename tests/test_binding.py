import pytest

from asserto import Asserto
from asserto import assertable

from .markers import NO_UNTRIGGERED_WARNINGS


def is_length_five(self):
    try:
        if len(self.actual) != 5:
            self.error(f"{self.actual} was not length 5!")
    except TypeError:
        self.error(f"{self.actual} was not sizable; it had no `__len__`")


@pytest.fixture(scope="function")
def bind_function(request) -> None:
    """
    Bind a function and undo it after.
    :param request:
    """
    assertable(is_length_five)
    request.addfinalizer(lambda: delattr(Asserto, is_length_five.__name__))


@pytest.mark.usefixtures("bind_function")
def test_binding_successful(asserto) -> None:
    assertable(is_length_five)
    asserto([1, 2, 3, 4, 5]).is_length_five()


@NO_UNTRIGGERED_WARNINGS
def test_calling_unbound(asserto) -> None:
    with pytest.raises(AttributeError) as error:
        asserto(5).is_length_five()
    asserto(error.value.args[0]).is_equal_to("unknown assertion method: is_length_five")


def test_cannot_register_lambda(asserto) -> None:
    expected = "Binding functions does not support lambdas, they have no name"
    asserto(assertable).should_raise(ValueError).when_called_with(reason=expected, func=lambda: ...)


def test_no_name(asserto) -> None:
    class C:
        ...

    expected = "Binding functions must be of function types."
    asserto(assertable).should_raise(ValueError).when_called_with(reason=expected, func=C)


def test_ends_with_is(asserto) -> None:
    def foo_is(self):
        ...

    asserto(assertable).should_raise(ValueError).when_called_with(
        reason="Binding functions cannot end with `_is`", func=foo_is
    )


@pytest.fixture
def wrapped_fn(request):
    @assertable
    def my_fn(self):
        ...

    request.addfinalizer(lambda: delattr(Asserto, my_fn.__name__))


@pytest.mark.usefixtures("wrapped_fn")
def test_decorator_binds(asserto) -> None:
    asserto(5).my_fn()