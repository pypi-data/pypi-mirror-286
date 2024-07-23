# Struct Types

Validate your classes against interfaces the familiar way, just import `does`

## Example

```python
from abc import abstractmethod
from typing import Protocol, runtime_checkable

from does import does

@runtime_checkable
class Notifier(Protocol):
    @abstractmethod
    def notify(self):
        pass


class EmailService:
    def __init__(self):
        does(Notifier).match(EmailService)
        # Type mismatch; EmailService does not implement .notify
```
