from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.provider.sink.test.test_sink import TestSink


class TestSinkParser(SinkParser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return TestSink(config["dataSourceRefs"])