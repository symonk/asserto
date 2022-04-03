import pytest

from asserto import assert_that


@pytest.fixture
def asserto():
    return assert_that
