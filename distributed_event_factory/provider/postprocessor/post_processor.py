import abc
from typing import Any

from process_mining_core.datastructure.core.event import Event


class PostProcessor:
    @abc.abstractmethod
    def process(self, event: "Event") -> Any:
        pass
