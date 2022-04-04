import pytest

from asserto import asserto as assert_factory


@pytest.fixture
def asserto():
    return assert_factory
