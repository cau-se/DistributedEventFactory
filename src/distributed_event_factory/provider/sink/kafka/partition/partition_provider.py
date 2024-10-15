from abc import ABC, abstractmethod
from distributed_event_factory.core.event import Event


class PartitionProvider(ABC):
    @abstractmethod
    def get_partition(self, event: Event):
        pass

