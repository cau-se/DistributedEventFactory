from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.uniform_selction_provider import UniformEventSelectionProvider


class UniformEventSelectionParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return UniformEventSelectionProvider(
            potential_events=self.dependencies[config["type"]].parse(config["eventData"])
        )