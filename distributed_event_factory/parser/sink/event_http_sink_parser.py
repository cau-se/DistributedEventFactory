from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.http.http_sink import EventHttpSink


class EventHttpSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return EventHttpSink(
            url=config["url"],
            data_source_ref=config["dataSourceRefs"],
        )
