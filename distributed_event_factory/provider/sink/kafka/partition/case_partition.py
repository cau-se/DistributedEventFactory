from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.kafka.partition.partition_provider import PartitionProvider


class CaseIdPartitionProvider(PartitionProvider):
    def __init__(self, number_of_partitions):
        self.max_number_of_partitions = number_of_partitions

    def get_partition(self, event: Event) -> int:
        return hash(event.get_case()) % self.max_number_of_partitions
