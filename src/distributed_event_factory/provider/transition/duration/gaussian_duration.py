import random

from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider


class GaussianDurationProvider(DurationProvider):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def get_duration(self):
        return random.gauss(mu=self.mu, sigma=self.sigma)