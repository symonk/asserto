from asserto._mixins import AsserterMixin


class AssertsBooleans(AsserterMixin):
    def __init__(self, actual: bool) -> None:
        self.actual = actual

    def is_true(self) -> None:
        """
        Checks the actual value evaluates to `True`.
        """
        if not self.actual:
            self.error(f"{self.actual!r} was not True")

    def is_false(self) -> None:
        """
        Checks the actual value evaluates to `False`.
        :return:
        """
        if self.actual:
            self.error(f"{self.actual!r} was not False")
