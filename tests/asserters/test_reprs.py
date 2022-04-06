from asserto.assertors import AssertsRegex
from asserto.assertors import AssertsStrings


def test_repr_regex(asserto) -> None:
    asserto(repr(AssertsRegex("example"))).is_equal_to("AssertsRegex(actual='example')")


def test_repr_strings(asserto) -> None:
    asserto(repr(AssertsStrings("example"))).is_equal_to("AssertsStrings(actual='example')")
