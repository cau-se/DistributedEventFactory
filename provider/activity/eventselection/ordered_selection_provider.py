from typing import List

from provider.activity.eventselection.event_selection_provider import EventSelectionProvider
from provider.event.event_provider import EventDataProvider


class OrderedEventSelectionProvider(EventSelectionProvider):

    def __init__(self, potential_events: List[EventDataProvider]):
        self.potential_events = potential_events
        self.state = 0

    def get_event_data(self):
        event = self.potential_events[self.state % len(self.potential_events)]
        self.state += 1
        return event



