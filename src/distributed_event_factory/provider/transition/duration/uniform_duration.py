import random

from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider


class UniformDurationProvider(DurationProvider):

    def __init__(self, lower_bound, upper_bound):
        self.lower_border = lower_bound
        self.upper_border = upper_bound

    def get_duration(self):
        return random.uniform(self.lower_border, self.upper_border)
