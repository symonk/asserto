# Welcome to the documentation for `Asserto`.

## Quick Start

`Asserto` can be installed with pip:

```bash
pip install asserto
```

Then import `assert_that` to get started:

```python
from asserto import assert_that

def test_something() -> None:
    assert_that("Hello").has_length(5).matches(r"\w{5}$").ends_with("lo").starts_with("Hel")

```