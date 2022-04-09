import pytest

from asserto._asserto import Reason


@pytest.mark.parametrize(
    "reason_obj, reason_txt, expected",
    [
        (Reason("cat_no_desc"), "reason", "[cat_no_desc] reason"),
        (Reason("cat", "desc"), "reason", "[cat] desc"),
        (Reason(), "reason", "reason"),
    ],
)
def test_basic_reason(asserto, reason_obj, reason_txt, expected) -> None:
    asserto(reason_obj.format(reason_txt)).is_equal_to(expected)
