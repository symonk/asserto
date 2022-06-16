# Welcome to the documentation for `Asserto`.

## Usage

Asserto is a simple assertion library to add flexibility and fluency into assertions.  Asserto
makes assertion writing powerful yet effortless for the more complex scenarios.  Check out some
examples below:

#### Fluent API:

`Asserto` exposes a fully fluent API for chaining assertions against a value.

```python
from asserto import asserto


def test_multiple_assert_fluency() -> None:
    asserto("Hello").has_length(5).match(r"\w{5}$").ends_with("lo").starts_with("Hel")
```

----

#### Soft Assertions:


`Asserto` Has `soft` capabilities; allowing multiple assertions to be performed before failing with a
summary of the failures.

```python
from asserto import asserto

def test_baz() -> None:
    with asserto("Baz") as context:
        # asserto when used in a python context is run in 'soft' mode;
        # upon exiting the context; congregated errors are subsequently raised (if any)
        context.starts_with("B").ends_with("z").is_equal_to("Baz").has_length(2)  # Ends in a failure.
```

Will result in the following:

```shell
    def test_foo(asserto) -> None:
>       with asserto("Bar") as context:
E       AssertionError: 1 Soft Assertion Failures
E       [AssertionError("Length of: 'Bar' was not equal to: 2")]
```

-----

#### Exception Handling:

`Asserto` has the ability to assert exceptions are raised on `callables` using a simple API.

```python
from asserto import asserto
import typing


def simple_callable(x: int) -> typing.NoReturn:
    raise ValueError(x)


def test_exc_handling():
    asserto(simple_callable).should_raise(ValueError).when_called_with(x=25)
```

-----

#### Dynamic Lookups:

`Asserto` has the ability to dynamically lookup attributes on any object type.  This is
handled using the `attr_is(expected)` syntax.

```python
from asserto import asserto


class Foo:

    def __init__(self, x) -> None:
        self.x = x

    def double_x(self) -> int:
        return self.x * 2


def test_foo_dynamically() -> None:
     # dynamically looking up `x` (attr) or `double_x` bound method & invoking it!
    asserto(Foo(10)).x_is(10).double_x_is(20)
```

-----

#### Dynamic assert registration

`Asserto` allows users to easily bolt on their assertion functions.

```python
from asserto import asserto
from asserto import register_assert


@register_assert  # Option 1.
def custom_assert(self):
    if self.actual != 5:
        self.check_should_raise(f"{self.actual} did not equal five!")


register_assert(custom_assert)  # Option 2


def test_user_defined_callables() -> None:
    asserto(6).custom_assert()
```

yields the following:

```console
E       AssertionError: 6 did not equal five!
```

-----
