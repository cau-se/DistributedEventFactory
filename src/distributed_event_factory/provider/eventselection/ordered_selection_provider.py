from typing import List

from distributed_event_factory.provider.event.event_provider import EventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider


class OrderedEventSelectionProvider(EventSelectionProvider):

    def __init__(self, potential_events: List[EventDataProvider]):
        self.potential_events = potential_events
        self.state = 0

    def get_event_data(self):
        event = self.potential_events[self.state % len(self.potential_events)]
        self.state += 1
        return event



