from typing import List

from src.distributed_event_factory.provider.event.event_provider import EventDataProvider
from src.distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider


class UniformEventSelectionProvider(EventSelectionProvider):
    def __init__(self, potential_events: List[EventDataProvider]):
        self.potential_events = potential_events

    def get_event_data(self):
        import random
        return self.potential_events[int(random.uniform(0, len(self.potential_events)))]
