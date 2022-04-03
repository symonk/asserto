import pytest

from asserto import asserto as Asserto


@pytest.fixture
def asserto():
    return Asserto
