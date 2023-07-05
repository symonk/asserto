from asserto import asserto
from asserto._templates import CallableTemplate


def test_is_subbed() -> None:
    asserto(CallableTemplate("$actual is $expected")(actual="f", expected="b")).is_equal_to("f is b")
