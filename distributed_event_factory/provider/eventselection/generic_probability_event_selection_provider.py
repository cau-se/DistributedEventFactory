from typing import List

from numpy import random

from distributed_event_factory.provider.event.event_provider import EventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider

class GenericProbabilityEventSelectionProvider(EventSelectionProvider):

    def __init__(self, probability_distribution: List[float], potential_events: List[EventDataProvider]):
        self.probability_distribution = probability_distribution
        self.potential_events = potential_events

    def get_event_data(self):
        index = random.choice(len(self.potential_events), p=self.probability_distribution)
        return self.potential_events[index]
