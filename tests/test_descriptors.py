import re

from asserto.descriptors import IsCallable
from asserto.descriptors import IsInstanceOf


def test_instance_of(asserto) -> None:
    asserto(IsInstanceOf(int).validate).should_raise(ValueError).when_called_with(value="25")
    asserto(IsInstanceOf(str, re.Pattern).validate).should_raise(ValueError).when_called_with(value=None)


def test_is_callable(asserto) -> None:
    asserto(IsCallable().validate).should_raise(ValueError).when_called_with(value=None)
