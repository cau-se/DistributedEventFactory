from abc import ABC, abstractmethod
from typing import List

from provider.activity.activity_provider import DistinctActivityProvider
from provider.activity.selection.activity_selection_provider import ActivitySelectionProvider
from provider.event.event_data import EventData
from provider.transition.duration.duration_provider import DurationProvider, StaticDurationProvider
from provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, DistinctNextSensorProvider


class EventDataProvider(ABC):

    @abstractmethod
    def get_event_data(self):
        pass


class ConcreteEventDataProvider(EventDataProvider):
    def __init__(self, list_of_events: List[EventDataProvider]):
        self.index = 0
        self.list_of_events = list_of_events

    def get_event_data(self):
        self.index = (self.index + 1) % len(self.list_of_events)
        return self.list_of_events[self.index].get_event_data()


class CustomEventDataProvider(EventDataProvider):
    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivitySelectionProvider,
            transition_provider: NextSensorProvider
    ):
        self.duration_provider = duration_provider
        self.activity_provider = activity_provider
        self.transition_provider = transition_provider

    def get_event_data(self):
        return EventData(
            self.duration_provider,
            self.activity_provider,
            self.transition_provider
        )

    def get_activity(self):
        return self.activity_provider.emit_activity()

    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_next_sensor(self):
        return self.transition_provider.get_next_sensor()


class StartEventProvider(EventDataProvider):

    def get_event_data(self):
        return EventData(
            StaticDurationProvider(0),
            DistinctActivityProvider("start"),
            DistinctNextSensorProvider(0),
        )


class EndEventProvider(EventDataProvider):
    def get_event_data(self):
        return EventData(
            StaticDurationProvider(0),
            DistinctActivityProvider("end"),
            DistinctNextSensorProvider(0),
        )
