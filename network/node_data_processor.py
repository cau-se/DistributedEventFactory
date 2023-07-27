import abc
from typing import List

from utils.utils_types import SensorLog


class NodeDataProcessor(metaclass=abc.ABCMeta):
    def __init__(self):
        self.CACHE_IS_READY: bool = True
        self.CACHE_LENGTH: int = 0

    @abc.abstractmethod
    def generate_cache(self, cache_length: int) -> List[SensorLog]:
        pass

    @abc.abstractmethod
    def init_cache_generation(self):
        pass
