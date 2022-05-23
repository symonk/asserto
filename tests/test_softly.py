import re

import pytest


def test_multiple_soft_assertions(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        with asserto(100) as a:
            a.is_equal_to(99).is_equal_to(101)
    assert asserto(str(error.value.args[0])).match(
        ".*2 Soft Assertion Failures.*100 is not equal to: 99.*100 is not equal to: 101.*", re.S
    )
