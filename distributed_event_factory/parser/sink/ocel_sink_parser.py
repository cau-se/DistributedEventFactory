from distributed_event_factory.parser.parser import Parser
from provider.sink.ocel.ocel_sink import OcelConsole


class OcelConsoleSinkParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return OcelConsole(config["id"], config["dataSourceRefs"])