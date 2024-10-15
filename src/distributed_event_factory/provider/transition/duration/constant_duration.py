from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider

class ConstantDurationProvider(DurationProvider):
    def __init__(self, duration):
        self.duration = duration

    def get_duration(self):
        return self.duration
