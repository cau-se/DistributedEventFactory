from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.eventselection.ordered_selection_provider import OrderedEventSelectionProvider


class OrderedEventSelectionParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return OrderedEventSelectionProvider(config["eventData"])