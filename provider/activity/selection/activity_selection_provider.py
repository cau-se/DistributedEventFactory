from abc import ABC, abstractmethod
import random
from typing import List

from core.event import Activity
from provider.activity.generation.activity_generation_provider import ActivityGenerationProvider


class ActivitySelectionProvider(ABC):
    @abstractmethod
    def emit_activity(self, payload: int):
        pass


class ActivitySelectionProviderFactory:

    @abstractmethod
    def get_activity_provider(self) -> ActivitySelectionProvider:
        pass


