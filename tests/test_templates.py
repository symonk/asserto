from asserto._templates import CallableTemplate


def test_is_subbed(asserto) -> None:
    asserto(CallableTemplate("$actual is $expected")(actual="f", expected="b")).is_equal_to("f is b")
