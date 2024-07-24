from .unit import does


class ProtocolUnion[Protocol]:
    def __init__(self, *_: type[Protocol]):
        pass

    def on(self, _: type[Protocol]):
        """"""


def union[Protocols](*protocols: type[Protocols]) -> ProtocolUnion[Protocols]:
    """
    Hint static type analysis tools if the provided type correctly implements one of the
    protocols in the union.
    """
    return ProtocolUnion(*protocols)


def interfaces[*Interfaces](*protocols: * tuple[*Interfaces]) -> tuple[*Interfaces]:
    """
    Syntactic sugar/DSL that explicitly indicates code checking the correctness of
    a class's interface.
    """
    return protocols


implements = does
