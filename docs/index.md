# Welcome to the documentation for `Asserto`.

## Usage

Asserto is a simple assertion library to add flexibility and fluency into assertions.  Asserto
makes assertion writing powerful yet effortless for the more complex scenarios.  Check out some
examples below:

``` { .python .annotate }
from asserto import asserto


def test_something():
    asserto((5, 6, 7)).is_length(3).equals((5,6,7))

# Or if you are using the `asserto-pytest` plugin:
def test_with_pytest(asserto):
    asserto("Hello").is_length(11).matches(r"^[A-Z][a-z]{4}$")
```
