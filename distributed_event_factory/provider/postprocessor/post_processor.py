import abc
from typing import Any

class PostProcessor:
    @abc.abstractmethod
    def process(self, event: "Event") -> Any:
        pass

    def flush(self):
        """Return any events held back by a stateful processor."""
        return []
