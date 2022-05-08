class Handler:
    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if callable(attr):
            # The attribute is a bound method; automatically guard it by invoking accept()
            self.accept()
