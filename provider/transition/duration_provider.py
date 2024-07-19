import random
from abc import abstractmethod


class DurationProvider:

    @abstractmethod
    def get_duration(self):
        pass


class UniformDurationProvider(DurationProvider):

    def __init__(self, lower_bound, upper_bound):
        self.lower_border = lower_bound
        self.upper_border = upper_bound

    def get_duration(self):
        return random.uniform(self.lower_border, self.upper_border)


class StaticDurationProvider(DurationProvider):
    def __init__(self, duration):
        self.duration = duration

    def get_duration(self):
        return self.duration


class GaussianDurationProvider(DurationProvider):
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def get_duration(self):
        return random.gauss(mu=self.mu, sigma=self.sigma)

class DurationProviderRegistry(DurationProvider):
    def get(self, type: str, args) -> DurationProvider:
        registry = dict()
        registry["static"] = lambda config: StaticDurationProvider(config["duration"])
        registry["uniform"] = lambda config: UniformDurationProvider(config["lower_bound"], config["upper_bound"])
        registry["gaussian"] = lambda config: GaussianDurationProvider(config["mu"], config["sigma"])
        return registry[type](args)
