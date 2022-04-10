class Dynamic:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(**kwargs)

    def __repr__(self) -> str:
        return str(self.__dict__)
