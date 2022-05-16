class Handler:
    @staticmethod
    def dispatch_and_raise(fn, expected, error, *args, **kwargs):
        """
        Dispatches a call to an underlying callable and if the return value of the function
        is not equal to expected, raises an AssertionError.
        """
        if fn(*args, **kwargs) != expected:
            raise AssertionError(error)
