from abc import ABC, abstractmethod

from distributed_event_factory.core.event import AbstractEvent, Event


class PartitionProvider(ABC):
    @abstractmethod
    def get_partition(self, event: AbstractEvent) -> int:
        pass


class ConstantPartitionProvider(PartitionProvider):

    def __init__(self, partition):
        self.partition = partition

    def get_partition(self, event):
        return self.partition


class CaseIdPartitionProvider(PartitionProvider):
    def __init__(self, max_number_of_partitions):
        self.max_number_of_partitions = max_number_of_partitions

    def get_partition(self, event: Event) -> int:
        return hash(event.case_id) % self.max_number_of_partitions


