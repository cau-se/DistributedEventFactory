from abc import ABC, abstractmethod

from process_mining_core.datastructure.core.event import Event


class PartitionProvider(ABC):
    @abstractmethod
    def get_partition(self, event: Event):
        pass

