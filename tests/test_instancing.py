import pytest

from .utility.instance_checks import DirectSubklazz
from .utility.instance_checks import IndirectSubklazz
from .utility.instance_checks import Klazz
from .utility.instance_checks import VirtualSubklazz


def test_direct_instance_of() -> None:
    asserto(DirectSubklazz()).is_instance(Klazz)
    asserto(DirectSubklazz()).is_instance((Klazz,))


def test_indirect_instance_of() -> None:
    asserto(IndirectSubklazz()).is_instance(Klazz)
    asserto(IndirectSubklazz()).is_instance((Klazz,))


def test_virtual_instance_of() -> None:
    asserto(VirtualSubklazz()).is_instance(Klazz)
    asserto(VirtualSubklazz()).is_instance((Klazz,))


def test_not_an_instance() -> None:
    with pytest.raises(AssertionError) as error:
        asserto(25).is_instance(Klazz)
    asserto(error.value.args[0]).match(r"25 was not an instance of.*instance_checks.Klazz.*")
