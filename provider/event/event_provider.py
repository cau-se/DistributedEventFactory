from abc import ABC, abstractmethod

from provider.activity.generation.activity_generation_provider import ActivityGenerationProvider
from provider.transition.duration.duration_provider import DurationProvider
from provider.transition.transition_provider import TransitionProvider


class EventProvider(ABC):
    @abstractmethod
    def get_event(self):
        pass


class CustomEventProvider(EventProvider):

    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivityGenerationProvider,
            transition_provider: TransitionProvider
    ):
        self.duration_provider = duration_provider
        self.activity_provider = activity_provider
        self.transition_provider = transition_provider


    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_next_sensor(self):
        return self.transition_provider.get_next_sensor()

    def get_activity(self):
        return self.activity_provider.get_activities()
