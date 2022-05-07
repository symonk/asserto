class _HandlerMeta(type):
    """
    A Metaclass for handlers that automatically delegates verification methods through
    their `accepts` implementation on each call.  Any handler using this Metaclass
    should implement `accept` which checks `n` predicates to conclude if the handler
    of that type can support assertion checks on the actual value provided.
    """

    ...


class Handler(metaclass=_HandlerMeta):
    """
    A subclass for handlers to hide the magic of the MetaClass.
    Handlers should subclass this directly.
    """

    ...
