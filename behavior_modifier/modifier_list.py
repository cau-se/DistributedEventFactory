from abc import ABC, abstractmethod
from typing import List
from random import shuffle
from utils.types import SensorLog


class BaseBehaviorModifier(ABC):
    @abstractmethod
    def mutate_cache(self, cache: List[SensorLog]) -> List[SensorLog]:
        pass


class NoiseBehaviorModifier(BaseBehaviorModifier):
    def __init__(self, frequency: float):
        self.frequency = frequency

    def mutate_cache(self, cache: List[SensorLog]) -> List[SensorLog]:
        return cache


class OutlierBehaviorModifier(BaseBehaviorModifier):
    def __init__(self, type: str, frequency: float):
        self.frequency = frequency
        self.type = type

    def mutate_cache(self, cache: List[SensorLog]) -> List[SensorLog]:
        return cache


class RandomizeBehaviorModifier(BaseBehaviorModifier):
    def mutate_cache(self, cache: List[SensorLog]) -> List[SensorLog]:
        cache_randomized = cache
        shuffle(cache_randomized)
        return cache_randomized
