from asserto import asserto
from asserto.handlers._numeric import NumberHandler


def test_handler_repr_is_correct():
    asserto(repr(NumberHandler(100))).is_equal_to("NumberHandler(actual=100)")
