import pytest

from asserto import Asserto
from asserto import register_assert


def is_length_five(self):
    try:
        if len(self.actual) != 5:
            self.check_should_raise(f"{self.actual} was not length 5!")
    except TypeError:
        self.check_should_raise(f"{self.actual} was not sizable; it had no `__len__`")


@pytest.fixture(scope="function")
def bind_function(request) -> None:
    """
    Bind a function and undo it after.
    :param request:
    """
    register_assert(is_length_five)
    request.addfinalizer(lambda: delattr(Asserto, is_length_five.__name__))


@pytest.mark.usefixtures("bind_function")
def test_binding_successful(asserto) -> None:
    register_assert(is_length_five)
    asserto([1, 2, 3, 4, 5]).is_length_five()


def test_calling_unbound(asserto) -> None:
    with pytest.raises(AttributeError) as error:
        asserto(5).is_length_five()
    asserto(error.value.args[0]).is_equal_to("unknown assertion method: is_length_five")


def test_cannot_register_lambda(asserto) -> None:
    expected = "Binding functions does not support lambdas, they have no name"
    asserto(register_assert).should_raise(ValueError, match=expected).when_called_with(func=lambda: ...)


def test_no_name(asserto) -> None:
    class C:
        ...

    expected = "Binding functions must be of function types."
    asserto(register_assert).should_raise(ValueError, match=expected).when_called_with(func=C)


def test_ends_with_is(asserto) -> None:
    def foo_is(self):
        ...

    expected = "Binding functions cannot end with `_is`"
    asserto(register_assert).should_raise(ValueError, match=expected).when_called_with(func=foo_is)


@pytest.fixture
def wrapped_fn(request):
    @register_assert
    def my_fn(self):
        ...

    request.addfinalizer(lambda: delattr(Asserto, my_fn.__name__))


@pytest.mark.usefixtures("wrapped_fn")
def test_decorator_binds(asserto) -> None:
    asserto(5).my_fn()
