from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.kafka.partition.case_partition import CaseIdPartitionProvider

class CasePartitionParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return CaseIdPartitionProvider(number_of_partitions=config["partitionCount"])