import random

from distributed_event_factory.provider.payload.payload_update_provider import PayloadUpdateProvider


class UniformPayloadUpdateProvider(PayloadUpdateProvider):
    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_payload_delta(self):
        return random.uniform(self.lower_bound, self.upper_bound)
