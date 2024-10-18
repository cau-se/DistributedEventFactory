from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.generic_probability_event_selection_provider import \
    GenericProbabilityEventSelectionProvider


class GenericProbabilityEventSelectionParser(Parser):
    def __init__(self):
        self.dependencies=dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return GenericProbabilityEventSelectionProvider(
            self.dependencies["distribution"].parse(config["distribution"]),
            self.dependencies["eventData"].parse(config["eventData"])
        )