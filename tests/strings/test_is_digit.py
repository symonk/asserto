from asserto import asserto

def test_is_digit() -> None:
    asserto("12345").is_digit()