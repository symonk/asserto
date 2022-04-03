![Asserto](.github/images/logo.png)

![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)
### Asserto

Python assertions made fluent and easy.

    - Chained and fluent assertions.
    - Soft & Hard assertions.
    - Clear, rich diffs to identify failure reasons easily.
    - Extensibility, add your own easily.
    - More...

## Getting Started

```python
from asserto import asserto


def test_something():
    asserto((5, 6, 7)).is_length(3)


# Or use our pytest fixture

def test_with_pytest(asserto):
    asserto(25).is_instance_of(int)
    asserto("Hello World").matches(r"^[A-Z][a-z]{4} [A-Z][a-z]{4}$")

```

Asserto is current in its early development stages; contributions are extremely welcome!
Check out our `CONTRIBUTING.md` to get started.
