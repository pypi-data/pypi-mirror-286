class Interface[Protocol]:

    __protocol: type[Protocol]

    def __init__(self, protocol: type[Protocol], /):
        """
        Example:

        ```py
        class Foo:
            def __init__(self):
                does(Protocol).match(Foo)
        ```
        """
        self.__protocol = protocol

    def compile(self, type: type[Protocol]):
        """
        Analyze if the provided type correctly implements the protocol, raising an
        exception if a type mismatch is found.
        """

        if isinstance(type, self.__protocol) == False:
            raise TypeError

        return self.on(type)

    def on(self, type: type[Protocol] | Protocol):
        """
        Hint static type analysis tools to check if the provided type correctly
        implements the protocol.
        """
        _ = type

        return self.__protocol


def does[I](protocol: type[I]) -> Interface[I]:
    return Interface(protocol)


of = does
