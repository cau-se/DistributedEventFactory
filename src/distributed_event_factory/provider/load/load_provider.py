import abc


class LoadProvider:

    @abc.abstractmethod
    def get_load_value(self):
        pass


class ConstantLoadProvider(LoadProvider):

    def __init__(self, intensity):
        self.load = intensity

    def get_load_value(self):
        return self.load


class GradualIncreasingLoadProvider(LoadProvider):

    def __init__(self, tick_count_til_maximum_reached, minimal_load, maximal_load):
        self.load_parameter = 0
        self.tick_size = 1 / tick_count_til_maximum_reached
        self.maximal_load = maximal_load
        self.minimal_load = minimal_load

    def get_load_value(self):
        self.load_parameter += self.tick_size
        load = self.minimal_load + (self.maximal_load - self.minimal_load) * self.load_parameter
        return min(self.maximal_load, load)
