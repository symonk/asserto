from asserto._templates import CallableTemplate


def test_is_subbed(asserto) -> None:
    asserto(CallableTemplate("$foo is $bar")(foo="f", bar="b")).is_equal_to("f is b")
