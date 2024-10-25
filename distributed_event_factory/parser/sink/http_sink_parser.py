from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.http.http_sink import LoadTestHttpSink
from distributed_event_factory.provider.sink.ui.terminal_ui_sink import UiSink


class HttpSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return LoadTestHttpSink(
            url=config["url"],
            data_source_ref=config["dataSourceRefs"],
            frame_duration=config["timeframe"]
        )