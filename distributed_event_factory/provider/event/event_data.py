from distributed_event_factory.provider.activity.activity_provider import ActivityProvider
from distributed_event_factory.provider.payload.payload_update_provider import PayloadUpdateProvider
from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider
from distributed_event_factory.provider.transition.transition.transition_provider import TransitionProvider


class EventData:
    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivityProvider,
            transition_provider: TransitionProvider,
            payload_update_provider: PayloadUpdateProvider
    ):
        self.duration_provider = duration_provider
        self.activity_provider = activity_provider
        self.transition_provider = transition_provider
        self.payload_update_provider = payload_update_provider

    def get_duration(self):
        return self.duration_provider.get_duration()

    def get_next_sensor(self):
        return self.transition_provider.get_transition()

    def get_activity(self):
        return self.activity_provider.get_activity()

    def get_payload_delta(self):
        return self.payload_update_provider.get_payload_delta()
