from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.drifting_probability_event_selection_provider import \
    DriftingProbabilityEventSelectionProvider


class DriftingProbabilityEventSelectionParser(Parser):
    def __init__(self):
        self.dependencies=dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return DriftingProbabilityEventSelectionProvider(
            starting_probability_distribution=self.dependencies["distribution"].parse(config["startDistribution"]),
            end_probability_distribution=self.dependencies["distribution"].parse(config["endDistribution"]),
            steps=config["steps"],
            potential_events=self.dependencies["eventData"].parse(config["eventData"])
        )