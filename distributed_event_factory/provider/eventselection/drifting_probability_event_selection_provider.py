from typing import List

from numpy import random

from distributed_event_factory.provider.event.event_provider import EventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider

class DriftingProbabilityEventSelectionProvider(EventSelectionProvider):

    def __init__(self,
                 steps: int,
                 starting_probability_distribution: List[float],
                 end_probability_distribution: List[float],
                 potential_events: List[EventDataProvider]):
        self.starting_probability_distribution = starting_probability_distribution
        self.end_probability_distribution = end_probability_distribution
        self.potential_events = potential_events
        self.steps = steps
        self.step = 0

    def get_event_data(self):
        self.step = self.step + 1
        r = self.step / self.steps
        if r < 1:
            current_probability_distribution = []
            for i in range(len(self.starting_probability_distribution)):
                current_probability_distribution.append(r * self.starting_probability_distribution[i] + (1-r) * self.end_probability_distribution[i])
        else:
            current_probability_distribution = self.end_probability_distribution

        index = random.choice(len(self.potential_events), p=current_probability_distribution)
        return self.potential_events[index]
