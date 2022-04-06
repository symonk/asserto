from asserto import AssertTypes
from asserto.assertors import AssertsRegex
from asserto.assertors import AssertsStrings


def test_repr_regex(asserto) -> None:
    asserto(repr(AssertsRegex("example"))).is_equal_to("AssertsRegex(actual='example')")


def test_repr_strings(asserto) -> None:
    asserto(repr(AssertsStrings("example"))).is_equal_to("AssertsStrings(actual='example')")


def test_repr_soft(asserto) -> None:
    asserto(repr(asserto("foo", description="n"))).is_equal_to("Asserto(value=foo, type_of=hard, description=n)")
    asserto(repr(asserto(100))).is_equal_to("Asserto(value=100, type_of=hard, description=None)")
    asserto(repr(asserto(100, AssertTypes.SOFT))).is_equal_to("Asserto(value=100, type_of=soft, description=None)")
    asserto(repr(asserto(100, AssertTypes.WARN))).is_equal_to("Asserto(value=100, type_of=warn, description=None)")
