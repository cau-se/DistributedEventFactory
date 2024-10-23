from select import select

from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.provider.sink.kafka.kafka_sink import KafkaSink


class KafkaSinkParser(Parser):

    def __init__(self):
        super().__init__()
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return KafkaSink(
            config["bootstrapServer"],
            config["clientId"],
            config["topic"],
            self.dependencies["partition"].parse(config["partition"]),
            config["dataSourceRefs"]
        )