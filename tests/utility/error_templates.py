from asserto.mixins._const import ACTUAL_TYPE_ERROR


def invalid_actual_regex(actual, expected_types, method_name) -> str:
    """Returns the string template for type errors
    when the actual value is not as expected."""
    ACTUAL_TYPE_ERROR.format(actual, expected_types, method_name, type(actual))
