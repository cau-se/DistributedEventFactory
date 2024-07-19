import random
from abc import abstractmethod


class CountProvider:
    @abstractmethod
    def get(self):
        pass


class CountProviderRegistry:
    def get(self, config) -> CountProvider:
        registry = dict()
        registry["static"] = lambda config: StaticCountProvider(config["count"])
        registry["uniform"] = lambda config: UniformCountProvider(config["min"], config["max"])
        return registry[config["type"]](config)


class StaticCountProvider(CountProvider):
    def __init__(self, count):
        self.count = count

    def get(self):
        return self.count


class UniformCountProvider(CountProvider):
    def __init__(self, minimal_value, maximal_value):
        self.minimal_value = minimal_value
        self.maximal_value = maximal_value

    def get(self):
        return int(int(random.uniform(self.minimal_value, self.maximal_value)))
