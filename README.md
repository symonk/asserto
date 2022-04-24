![Asserto](.github/images/logo.png)

![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)
[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)

## Asserto

Asserto is a clean, fluent and powerful assertion library for python.  We recommend using `pytest` as a test
runner (as asserto has been developed using it internally) however any test runner will work just fine.  Using it
in your framework (non-test) code is also fine as well!

The main features of asserto are (and will be):

- Chaining and assertion fluency using a builder-esque API.
- Hard assertions by default; but soft when used in a python context.
- Clean, rich diffs to highlight problems and improve debuggability.
- Dynamicism, access underlying attributes and methods on pretty much any object using `attr_is(expected)` syntax.
- A robust set of APIs including all builtin types; files; regex and much, much more.
- Extensibility; registering your own assertion functions is easy! consider sending us a patch for useful ones.
- Automatic warnings in some cases of human error for assertions; i.e creating an instance but never checking anything.
- Much much more.

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
