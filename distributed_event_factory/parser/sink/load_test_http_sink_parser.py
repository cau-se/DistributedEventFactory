from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.loadtest.loadtest_sink import LoadTestHttpSink

class LoadTestHttpSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return LoadTestHttpSink(
            url=config["url"],
            data_source_ref=config["dataSourceRefs"],
            frame_duration=config["timeframe"]
        )