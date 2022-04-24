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


def test_described_as(asserto) -> None:
    with pytest.raises(AssertionError) as error:
        asserto(1).described_as("foo!").is_equal_to(2)
    asserto(error.value.args[0]).is_equal_to("foo!")


@pytest.mark.filterwarnings("ignore::asserto._warnings.NoAssertAttemptedWarning")
def test_described_updates_reason(asserto) -> None:
    foo = "foo"
    x = asserto(1).described_as(foo)
    asserto(x._reason.description).is_equal_to(foo)
