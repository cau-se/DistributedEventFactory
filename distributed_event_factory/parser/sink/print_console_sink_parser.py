from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.sink.console.console_sink import PrintConsole


class PrintConsoleSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return PrintConsole(config["id"], config["dataSourceRefs"])