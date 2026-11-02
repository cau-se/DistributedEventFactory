from typing import List

from distributed_event_factory.provider.event.event_provider import EventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider


class PayloadAwareEventSelectionProvider(EventSelectionProvider):
    def __init__(self, probability_distribution: List[float], potential_events: List[EventDataProvider]):
        self.probability_distribution = probability_distribution
        self.potential_events = potential_events
        self._validate()

    def _validate(self):
        if len(self.probability_distribution) != len(self.potential_events):
            raise ValueError("distribution and eventData must have the same length")
        if not self.probability_distribution:
            raise ValueError("distribution must not be empty")

        for probability in self.probability_distribution:
            if probability < 0:
                raise ValueError("distribution values must be >= 0")

        total = sum(self.probability_distribution)
        if total <= 0:
            raise ValueError("distribution sum must be > 0")

        if abs(total - 1.0) > 1e-9:
            raise ValueError("distribution sum must be 1.0 for payloadAware selection")

    def get_event_data(self, payload=None):
        if payload is None:
            raise ValueError("payloadAware selection requires a payload value")

        payload_value = min(100.0, max(0.0, float(payload)))
        quantile = payload_value / 100.0

        cumulative = 0.0
        for index, probability in enumerate(self.probability_distribution):
            cumulative += probability
            if quantile <= cumulative:
                return self.potential_events[index]

        return self.potential_events[-1]
