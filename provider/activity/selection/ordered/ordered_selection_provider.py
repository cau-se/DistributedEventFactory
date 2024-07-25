from typing import List

from core.event import Activity
from provider.activity.generation.activity_generation_provider import ActivityGenerationProvider
from provider.activity.selection.activity_selection_provider import ActivitySelectionProviderFactory, \
    ActivitySelectionProvider


class OrderedActivitySelectionProviderFactory(ActivitySelectionProviderFactory):

    def __init__(self, potential_activities_provider: ActivityGenerationProvider):
        self.potential_activities_provider = potential_activities_provider

    def get_activity_provider(self) -> ActivitySelectionProvider:
        return OrderedActivitySelectionProvider(self.potential_activities_provider.get_activities())


class OrderedActivitySelectionProvider(ActivitySelectionProvider):
    def __init__(self, potential_activities: List[Activity]):
        self.potential_activities = potential_activities
        self.state = 0

    def emit_activity(self, payload: int) -> Activity:
        activity = self.potential_activities[self.state % len(self.potential_activities)]
        self.state += 1
        return activity
