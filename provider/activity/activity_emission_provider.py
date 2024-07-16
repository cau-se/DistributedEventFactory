from abc import ABC, abstractmethod
import random
from typing import List

from core.event import Activity
from provider.activity.activity_generation_provider import ActivityGenerationProvider


class ActivityEmissionProvider(ABC):
    @abstractmethod
    def emit_activity(self, payload: int):
        pass


class ActivityEmissionProviderFactory:

    @abstractmethod
    def get_activity_provider(self) -> ActivityEmissionProvider:
        pass


class UniformActivityEmissionProviderFactory(ActivityEmissionProviderFactory):

    def __init__(self, potential_activities_provider: ActivityGenerationProvider):
        self.potential_activities_provider = potential_activities_provider

    def get_activity_provider(self) -> ActivityEmissionProvider:
        return UniformActivityEmissionProvider(self.potential_activities_provider.get_activities())


class UniformActivityEmissionProvider(ActivityEmissionProvider):
    def __init__(self, potential_activities: List[Activity]):
        self.potential_activities = potential_activities

    def emit_activity(self, payload: int) -> Activity:
        return self.potential_activities[int(random.uniform(0, len(self.potential_activities)) - 1)]
