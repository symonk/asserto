from asserto.handlers._numeric import NumberHandler
from asserto import asserto


def test_handler_repr_is_correct():
    asserto(repr(NumberHandler(100))).is_equal_to("NumberHandler(actual=100)")
