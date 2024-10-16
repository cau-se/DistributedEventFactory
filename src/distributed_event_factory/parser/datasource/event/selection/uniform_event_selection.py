from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.uniform_selction_provider import UniformEventSelectionProvider


class UniformEventSelectionParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return UniformEventSelectionProvider(
            potential_events=config["eventData"]
        )