from abc import ABC, abstractmethod

from provider.activity.generation.activity_generation_provider import ActivityGenerationProvider
from provider.activity.selection.activity_selection_provider import ActivitySelectionProvider
from provider.transition.duration.duration_provider import DurationProvider
from provider.transition.next_sensor_provider import NextSensorProvider
from provider.transition.transition_provider import TransitionProvider


class EventProvider(ABC):

    @abstractmethod
    def get_duration(self):
        pass

    @abstractmethod
    def get_next_sensor(self):
        pass

    @abstractmethod
    def get_activity(self):
        pass


class CustomEventProvider(EventProvider):

    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivitySelectionProvider,
            transition_provider: NextSensorProvider
    ):
        self.duration_provider = duration_provider
        self.activity_provider = activity_provider
        self.transition_provider = transition_provider

    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_next_sensor(self):
        return self.transition_provider.get_next_sensor()

    def get_activity(self):
        return self.activity_provider.emit_activity(payload=0)
