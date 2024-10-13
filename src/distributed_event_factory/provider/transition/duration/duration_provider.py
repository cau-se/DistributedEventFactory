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


class ConstantDurationProvider(DurationProvider):
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

