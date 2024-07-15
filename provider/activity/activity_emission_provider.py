import abc
from typing import List
import random


class ActivityEmissionProvider(abc.ABC):
    @abc.abstractmethod
    def emit_activity(self, payload: int):
        pass

class ActivityEmissionProviderFactory:

    @abc.abstractmethod
    def get_activity_provider(self, potential_activities) -> ActivityEmissionProvider:
        pass


class UniformActivityEmissionProviderFactory(ActivityEmissionProviderFactory):
    def get_activity_provider(self, potential_activities) -> ActivityEmissionProvider:
        return UniformActivityEmissionProvider(potential_activities)


class UniformActivityEmissionProvider(ActivityEmissionProvider):
    def __init__(self, potential_activities: List[str]):
        self.potential_activities = potential_activities

    def emit_activity(self, payload: int) -> str:
        return self.potential_activities[int(random.uniform(0, len(self.potential_activities)) - 1)]
