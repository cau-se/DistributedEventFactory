from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.payload_aware_event_selection_provider import \
    PayloadAwareEventSelectionProvider


class PayloadAwareEventSelectionParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return PayloadAwareEventSelectionProvider(
            self.dependencies["distribution"].parse(config["distribution"]),
            self.dependencies["eventData"].parse(config["eventData"])
        )
