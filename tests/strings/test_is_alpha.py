from asserto import asserto


def test_is_alpha(asserto) -> None:
    asserto("abcdef").is_alpha()