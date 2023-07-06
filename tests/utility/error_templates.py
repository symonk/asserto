from asserto._constants import MixinErrorTemplates


def invalid_actual_regex(actual, expected_types, method_name) -> str:
    """Returns the string template for type errors
    when the actual value is not as expected."""
    MixinErrorTemplates.ASSERTO_TYPE_ERROR.format(actual, expected_types, method_name, type(actual))
