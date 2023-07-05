import typing

import pytest

from asserto import Asserto
from asserto import assert_that


@pytest.fixture
def asserto() -> typing.Callable[[typing.Any], Asserto]:
    """This is unused because vscode cannot honour returned types correctly
    from pytest fixtures which makes intellisense in tests lackluster.  For this
    reason it is preferred to just import asserto into the test module rather than
    use this fixture."""
    return assert_that
