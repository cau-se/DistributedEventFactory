import abc
from typing import List

from utils.utils_types import SensorLog


class NodeDataProcessor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_cache(self, cache_length: int) -> List[SensorLog]:
        pass


