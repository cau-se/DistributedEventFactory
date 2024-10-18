from abc import ABC, abstractmethod
from typing import List

from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider, ActivityProvider
from distributed_event_factory.provider.event.event_data import EventData
from distributed_event_factory.provider.transition.duration.constant_duration import ConstantDurationProvider
from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider
from distributed_event_factory.provider.transition.transition.constant_transition import ConstantTransitionProvider
from distributed_event_factory.provider.transition.transition.transition_provider import TransitionProvider

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
            activity_provider: ActivityProvider,
            transition_provider: TransitionProvider
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
        return self.activity_provider.get_activity()

    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_transition(self):
        return self.transition_provider.get_transition()


class StartEventProvider(EventDataProvider):

    def __init__(self, transtition_provider):
        self.transtition_provider = transtition_provider

    def get_event_data(self):
        return EventData(
            ConstantDurationProvider(0),
            ConstantActivityProvider("start"),
            self.transtition_provider
        )


class EndEventProvider(EventDataProvider):
    def get_event_data(self):
        return EventData(
            ConstantDurationProvider(0),
            ConstantActivityProvider("end"),
            ConstantTransitionProvider(0)
        )
