from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.ui.terminal_ui_sink import UiSink


class UiSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return UiSink(config["id"], config["dataSourceRefs"])