import pytest

from .utility.instance_checks import DirectSubklazz
from .utility.instance_checks import IndirectSubklazz
from .utility.instance_checks import Klazz
from .utility.instance_checks import VirtualSubklazz


def test_direct_instance_of(asserto) -> None:
    asserto(DirectSubklazz()).is_instance(Klazz)
    asserto(DirectSubklazz()).is_instance((Klazz,))


def test_indirect_instance_of(asserto) -> None:
    asserto(IndirectSubklazz()).is_instance(Klazz)
    asserto(IndirectSubklazz()).is_instance((Klazz,))


def test_virtual_instance_of(asserto) -> None:
    asserto(VirtualSubklazz()).is_instance(Klazz)
    asserto(VirtualSubklazz()).is_instance((Klazz,))


def test_not_an_instance(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(25).is_instance(Klazz)
    asserto(error.value.args[0]).matches_beginning(r"^\[25\]: <class 'int'> was not an instance of:\s.*Klazz'>$")
