import re

from asserto.descriptors import EnforcedCallable
from asserto.descriptors import ValidatesInstanceOf


def test_instance_of(asserto) -> None:
    asserto(ValidatesInstanceOf(int).validate).should_raise(ValueError).when_called_with(value="25")
    asserto(ValidatesInstanceOf(str, re.Pattern).validate).should_raise(ValueError).when_called_with(value=None)


def test_is_callable(asserto) -> None:
    asserto(EnforcedCallable().validate).should_raise(ValueError).when_called_with(value=None)
