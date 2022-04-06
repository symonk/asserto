![Asserto](.github/images/logo.png)

![version](https://img.shields.io/pypi/v/asserto?color=%2342f54b&label=asserto&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/asserto/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/asserto)
[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/asserto/)
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
    asserto((5, 6, 7)).has_length(3).is_equal_to((5, 6, 7))


# Or if you are using the `asserto-pytest` plugin:
def test_with_pytest(asserto):
    asserto("Hello").has_length(5).matches(r"^[A-Z][a-z]{4}$")
```

Asserto is current in its early development stages; contributions are extremely welcome!
Check out our `CONTRIBUTING.md` to get started.
