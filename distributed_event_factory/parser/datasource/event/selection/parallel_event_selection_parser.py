from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.parallel_selection_provider import ParallelEventSelectionProvider


class ParallelEventSelectionParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return ParallelEventSelectionProvider(self.dependencies["eventData"].parse(config["eventData"]))