# Struct Types

Static + runtime class declaration level structural types/interface validation

In other words, the `implements` keyword from programming languages such as Typescript. Take better advantage of your protocols and be even more sure you correctly implement their interfaces, even in brownfield projects.

## Examples

### Explicit Syntax API

Recommended. Explicitly indicates code context without resorting to internal documentation or possibly unknown conventions.

```python
from struct_types import interfaces, implements

class EmailService:
    def __init__(self):
        interfaces(
            implements(Notifier).on(self),
            implements(Sender).on(self),
            implements(Object).on(self),
        )
```

### Succinct Syntax API

Terser alternative API.

```python
from struct_types import of

class EmailService:
    def __init__(self):
        of(Notifier).on(self)
        of(Sender).on(self)
        of(Object).on(self)
```

### Runtime API

Guard at runtime if a type correctly implements a protocol, raising an error if the types are mismatched. Note type hints are still defined for static type analysis and 3rd party library runtime type analysis.

```python
from struct_types import does

class EmailService:
    def __init__(self):
        does(Notifier).compile(EmailService)
        does(Sender).compile(EmailService)
        does(Object).compile(EmailService)
```

### Union API

Indicates the type must implement at least one of the protocols much like a union type.

```python
from struct_types import union

class EmailService:
    def __init__(self):
        union(Notifier, Sender, Object).on(EmailService)
```

**Note**: The `.on` method can interchangeably use either a reference to the type itself or an instance of a type. For consistency, prefer the co-locating within the constructor and using the reference to  `self`.

## See Also

- [Protocols](https://typing.readthedocs.io/en/latest/spec/protocol.html#protocols). These are Python's equivalent of `interface`s as found in other familiar programming languages such as Typescript and Java, and are the data structures that Struct Types has been designed for.
- [Beartype](https://pypi.org/project/beartype/) or [Pydantic](https://docs.pydantic.dev/latest/). Struct Types is not a replacement for runtime type and/or data validation.
