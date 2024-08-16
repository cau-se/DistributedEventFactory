import random
from typing import List

from provider.eventselection.event_selection_provider import EventSelectionProvider
from provider.event.event_provider import EventDataProvider


class UniformEventSelectionProvider(EventSelectionProvider):
    def __init__(self, potential_events: List[EventDataProvider]):
        self.potential_events = potential_events

    def get_event_data(self):
        return self.potential_events[int(random.uniform(0, len(self.potential_events)))]
