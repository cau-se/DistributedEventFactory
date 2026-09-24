import random

from distributed_event_factory.provider.payload.payload_update_provider import PayloadUpdateProvider


class GaussianPayloadUpdateProvider(PayloadUpdateProvider):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def get_payload_delta(self):
        return random.gauss(mu=self.mu, sigma=self.sigma)
