![Asserto](.github/images/logo.png)

![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)
[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)

## Asserto:

Asserto is a clean, fluent and powerful assertion library for python.  We recommend using `pytest` as a test
runner but asserto will work well with any test runner.

>Asserto was developed using pytest as it's test runner and has a `pytest-asserto` plugin that exposes asserto
>through a fixture.  Asserto will work on any runner or even without one.  Note: It is common practice for a
>test runner to apply assertion rewriting to change the behaviour of the `assert` keyword under the hood.

The main features of asserto are (and will be):

+ Chainable and Fluent API.
+ Ability for both `Hard` and `Soft` assertions.
+ Rich diffs to highlight problems, reduce churn and improve effeciency and debuggability.
+ Dynamic assertions; check any obj attribute or invoke any of it's function types.
+ Robust set of methods out of the box for common types.
+ Extensibility.  Bolt on your own assetions at runtime.
+ Human error detection, elaborate warnings when something is amiss.
+ Much more to come.

## Usage:

```python
from asserto import asserto

def test_foo() -> None:
    asserto("Hello").has_length(5).matches(r"\w{5}$").ends_with("lo").starts_with("Hel")
```

If you use pytest; a fixture is available for an `Asserto` factory function:

```python
def test_bar(asserto) -> None:  # No imports; just use the fixture.
    asserto("Hello").has_length(5).matches(r"\w{4}$").ends_with("lo").starts_with("Hel")
```

If you want to check many assertions in a single test without failing until after all:

```python
def test_baz(asserto) -> None:
    with asserto("Baz") as context:
        # asserto when used in a python context is run in 'soft' mode;
        # upon exiting the context; congregated errors are subsequently raised (if any)
        context.starts_with("B")
        context.ends_with("z")
        context.is_equal_to("Baz")
        context.is_length(2)  # Uh oh a failure!
```

Results in:

```shell
    def test_foo(asserto) -> None:
>       with asserto("Bar") as context:
E       AssertionError: 1 Soft Assertion Failures
E       [AssertionError("Length of: 'Bar' was not equal to: 2")]
```
