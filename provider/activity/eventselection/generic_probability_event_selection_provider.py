from typing import List

from numpy import random

from provider.activity.eventselection.event_selection_provider import EventSelectionProvider
from provider.event.event_provider import EventDataProvider

class GenericProbabilityEventSelectionProvider(EventSelectionProvider):

    def __init__(self, probability_distribution: List[float], potential_events: List[EventDataProvider]):
        self.potential_events = potential_events
        self.probability_distribution = probability_distribution

    def get_event_data(self):
        index = random.choice(len(self.potential_events), p=self.probability_distribution)
        return self.potential_events[index]
