import math

from distributed_event_factory.provider.load.load_provider import LoadProvider


class SinusLoadProvider(LoadProvider):
    def __init__(self, mean, amplitude, phase):
        self.i = 0
        self.mean = mean
        self.amplitude = amplitude
        self.phase = phase

    def get_load_value(self):
        self.i = self.i + 1
        return self.amplitude * math.sin(self.i * (math.pi / self.phase)) + self.mean
