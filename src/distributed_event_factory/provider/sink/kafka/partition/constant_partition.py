from distributed_event_factory.provider.sink.kafka.partition.partition_provider import PartitionProvider


class ConstantPartitionProvider(PartitionProvider):

    def __init__(self, partition):
        self.partition = partition

    def get_partition(self, event):
        return self.partition
