import typing

import pytest

from asserto import Asserto
from asserto import assert_that


@pytest.fixture
def asserto() -> typing.Callable[[], Asserto]:
    return assert_that
