from typing import List

from distributed_event_factory.provider.event.event_provider import EventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider


class ParallelEventSelectionProvider(EventSelectionProvider):

    def __init__(self, potential_events: List[EventDataProvider]):
        self.potential_events = potential_events

    def get_event_data(self):
        return self.potential_events