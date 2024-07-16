import random
import sys
from abc import abstractmethod


class CountProvider:

    @abstractmethod
    def get(self, max=sys.maxsize):
        pass


class StaticCountProvider(CountProvider):
    def __init__(self, count):
        self.count = count

    def get(self, max=sys.maxsize):
        if self.count > max:
            return max
        else:
            return self.count


class UniformCountProvider(CountProvider):
    def __init__(self, count):
        self.count = count

    def get(self, max=sys.maxsize):
        if self.count > max:
            return int(random.uniform(1, max))
        else:
            return int(int(random.uniform(1, self.count)))


