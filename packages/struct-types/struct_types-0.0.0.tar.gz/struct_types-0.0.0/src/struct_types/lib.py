class Implements[Protocol]:

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
        Hint Pyright to check if the implementation of the provided type is
        compatible with the Protocol's interface.
        """
        return type

    def match(self, type: type[Protocol]):
        """
        `.compile` the provided type, and raise an exception if it has received
        an incompatible type at runtime.
        """

        if isinstance(type, self.__protocol) == False:
            raise TypeError

        return self.compile(type)


def does[Interface](protocol: type[Interface]) -> Implements[Interface]:
    return Implements(protocol)


__all__ = ("does",)
