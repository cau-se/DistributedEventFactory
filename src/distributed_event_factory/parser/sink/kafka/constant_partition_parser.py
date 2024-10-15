from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.kafka.partition.constant_partition import ConstantPartitionProvider


class ConstantPartitionParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ConstantPartitionProvider(partition=config["partition"])