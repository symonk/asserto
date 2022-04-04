import abc


class Klazz(abc.ABC):
    ...


class DirectSubklazz(Klazz):
    ...


class IndirectSubklazz(DirectSubklazz):
    ...


class VirtualSubklazz:
    ...


Klazz.register(VirtualSubklazz)
