from provider.activity.activity_provider import ActivityProvider
from provider.transition.duration.duration_provider import DurationProvider
from provider.transition.nextsensor.next_sensor_provider import AbstractNextSensorProvider


class EventData:
    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivityProvider,
            transition_provider: AbstractNextSensorProvider
    ):
        self.duration_provider = duration_provider
        self.activity_provider = activity_provider
        self.transition_provider = transition_provider

    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_next_sensor(self):
        return self.transition_provider.get_next_sensor()

    def get_activity(self):
        return self.activity_provider.get_activity()
